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

# Keeps track of how fresh the coffee in the current pot is
class CoffeeFreshnessSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print "CoffeeFreshnessSession Joined the crossbar.io application session!"
        yield self.subscribe(self)
        yield self.register(self)

    @wamp.subscribe(u'com.makeandbuild.coffee.low')
    def low_coffee(self):
        print "The coffee is low. Should probably do something about that?"

    @wamp.subscribe(u'com.makeandbuild.coffee.brewing')
    def coffee_brewing(self):
        print "Fresh coffee is brewing right now hold your horses!"

    @wamp.subscribe(u'com.makeandbuild.coffee.refilled')
    def coffee_is_fresh(self):
        print "Alright there is fresh Coffee! Everyone should dash to the kitchen and get some before it is gone!"