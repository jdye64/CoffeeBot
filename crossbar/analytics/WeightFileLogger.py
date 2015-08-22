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

# Listens for the weight events and logs the data to a daily file so that analytics can later be ran.
class WeightFileLoggerSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print "WeightFileLoggerSession Joined the crossbar.io application session!"
        yield self.subscribe(self)
        yield self.register(self)

    # Receives the raw data about the weight from the DymoScale
    @wamp.subscribe(u'com.makeandbuild.coffee.weight')
    def log_coffee_weight(self, coffee_info):
        # Need to find the best way to efficiently write to a file in Python?
        print coffee_info