import sys
import os

# Adds the coffee root directory to the PYTHONPATH so that common modules can be shared.
# Note I know this is really ugly BUT crossbar.io has a bug where the PYTHONPATH cannot
# be set in the config.json currently
add_on_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))  # Gets 2 parents dirs up to the root folder
sys.path.append(add_on_dir)

from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from autobahn import wamp
import time

# Since most people start brewing the coffee and then just walk off this component is used to keep track of how long
# the coffee has been brewing and not on the scale. It asks the analytics engine to provide it with a average time
# that it usually takes for the Coffee to be brewed and then if that threshold is overreached post out a reminder to
# Slack for someone to go check that the coffee is brewed and place it on the scale.
class BrewingReminderSession(ApplicationSession):

    avg_brew_seconds = None
    start_timestamp = None

    @inlineCallbacks
    def onJoin(self, details):
        print "BrewingReminderSession Joined the crossbar.io application session!"

        self.avg_brew_seconds = yield self.call('com.makeandbuild.coffee.analytics.averagebrewseconds')

        yield self.subscribe(self)
        yield self.register(self)

    @wamp.subscribe(u'com.makeandbuild.coffee.brewing')
    @inlineCallbacks
    def coffee_brewing(self):
        if self.start_timestamp is None:
            # first time the brewing has been broadcast
            self.start_timestamp = time.time()
            print "Set self.start_timestamp: " + str(self.start_timestamp)
        else:
            # Check the AVG threshold hasn't been surpassed
            if self.avg_brew_seconds < (time.time() - self.start_timestamp):
                yield self.call('com.makeandbuild.coffee.brewing.reminder')


    @wamp.subscribe(u'com.makeandbuild.coffee.refilled')
    def reset_countdown_timer(self):
        self.start_timestamp = None