import sys
import os

# Adds the coffee root directory to the PYTHONPATH so that common modules can be shared.
# Note I know this is really ugly BUT crossbar.io has a bug where the PYTHONPATH cannot
# be set in the config.json currently
add_on_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))  # Gets 2 parents dirs up to the root folder
sys.path.append(add_on_dir)

from common.Slack import Slack
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from autobahn import wamp
from collections import deque

# This class is responsible for monitoring the level of the coffee in the pot while handling things like normalizing
# spikes in weight over a linear window of time. It will then be the main component to make decision and PUBlish
class CoffeeLevelMonitorSession(ApplicationSession):

    slack = Slack()
    message_history = deque(maxlen=20)  # Intervals are currently 2 seconds so this is 40 seconds worth of history
    being_refilled = False
    no_pot_present_raw_weight_threshold = 10 # Max number of raw ounces read from the weight if a pot isn't present
    coffee_low_weight = 8   # Number of ounces of coffee left in the pot considered low enough to need to be refilled.

    @inlineCallbacks
    def onJoin(self, details):
        print "CoffeeLevelMonitorSession Joined the crossbar.io application session!"
        yield self.subscribe(self)
        yield self.register(self)

    @wamp.subscribe(u'com.makeandbuild.coffee.weight')
    @inlineCallbacks
    def listen_for_coffee_weight(self, coffee_info):

        #print "Received Coffee_Info: " + str(coffee_info)

        if self.being_refilled:
            # In a refill state loop. Has raw_weight risen above no pot present threshold?
            if coffee_info["raw_weight"] > self.no_pot_present_raw_weight_threshold:
                # Coffee pot must have been refilled and placed on the scale again. Exit refill loop
                self.being_refilled = False
                yield self.publish('com.makeandbuild.coffee.refilled')
            else:
                yield self.publish('com.makeandbuild.coffee.brewing')
        else:
            # If the raw_weight is less than the no_pot_present threshold enter the being refilled loop
            if coffee_info["raw_weight"] < self.no_pot_present_raw_weight_threshold:
                self.being_refilled = True
                yield self.publish('com.makeandbuild.coffee.brewing')
            else:
                # Check the coffee_weight to see if it has fallen below the "low coffee" level that is configured
                if coffee_info["coffee_weight"] < self.coffee_low_weight:
                    yield self.publish('com.makeandbuild.coffee.low')

        # Appends the message to the local history
        self.message_history.append(coffee_info)