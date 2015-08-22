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

# Component that provides RPC(s) for informing other components of the current Coffee Session analytics
class AnalyticsSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print "AnalyticsSession Joined the crossbar.io application session!"
        yield self.subscribe(self)
        yield self.register(self)

    # Analyzes all previous data and computes the average brew time. This is an RPC that any other component can consume
    @wamp.register(u'com.makeandbuild.coffee.analytics.averagebrewseconds')
    def avg_brewseconds(self):
        print "Computing the Average Brew Time. Right now just returning 5 mins/300 seconds"
        return 300