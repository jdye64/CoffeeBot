from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn import wamp

class WAMPTestSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print "WAMP Test Session is online!"
        yield self.register(self)
        yield self.subscribe(self)

        brew_seconds = yield self.call('com.makeandbuild.coffee.analytics.averagebrewseconds')
        print "Average Brew Seconds: " + str(brew_seconds)

    @wamp.subscribe(u'com.makeandbuild.coffee.weight')
    def play_sound(self, weight_info):
        print "Weight: " + str(weight_info)


    @wamp.subscribe(u'com.makeandbuild.coffee.ibeacons')
    def listen_people_nearby(self, beacons):
        print "Beacons: " + str(beacons)

if __name__ == '__main__':
    runner = ApplicationRunner("ws://courier.makeandbuildatl.com:9015/ws", "coffee")
    runner.run(WAMPTestSession)