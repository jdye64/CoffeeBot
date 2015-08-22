# If you don't acutally have the USB scale nearby you can make a file and use this class to test your other components
# in certain scenarios
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep
from autobahn import wamp
import json

class ScaleMimicComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        print "ScaleMimicComponent has join the Crossbar.io Session"

        # Subscribes to the annotation defined RPC methods and PUB/SUB events
        yield self.register(self)
        yield self.subscribe(self)

        f = open('LowForOneMinute.txt', 'r')
        for line in f:
            json_data = json.loads(str(line).strip())
            print json_data
            yield self.publish('com.makeandbuild.coffee.weight', json_data)
            yield sleep(2)

        f.close()

        print "Finished sending all of the mimic weight events"

    @wamp.subscribe(u'com.makeandbuild.coffee.weight')
    def listen(self, details):
        print "Received something!"

if __name__ == '__main__':
    runner = ApplicationRunner("ws://courier.makeandbuildatl.com:9015/ws", "coffee")
    runner.run(ScaleMimicComponent)