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
from common.Slack import Slack
from common.PhraseEngine import Phrase
import random

# Component that decides who's turn it is to brew the coffee. Right now it is a simple algorithm but I want it to grow
# much more complex over time.
class BaristaSession(ApplicationSession):

    slack = Slack()

    tmp_threshold = 300
    remind_humor_threshold = tmp_threshold  # 5 min/300 sec before we remind them again if they haven't started brewing
    annoy_threshold = remind_humor_threshold + tmp_threshold
    negative_threshold = annoy_threshold + tmp_threshold

    humor_sent = False
    annoy_sent = False
    negative_sent = False

    start_timestamp = None
    current_barista = None

    @inlineCallbacks
    def onJoin(self, details):
        print "BaristaSession Joined the crossbar.io application session!"
        yield self.subscribe(self)
        yield self.register(self)

    @wamp.subscribe(u'com.makeandbuild.coffee.low')
    @inlineCallbacks
    def find_barista(self):
        if self.current_barista is None:
            self.start_timestamp = time.time()
            randint = random.randint(0, len(self.slack.members))
            self.current_barista = self.slack.members[8]        # Currently hardcoded to use Jeremy as the testing user
            print "Barista Chosen: " + str(self.current_barista.id) + " Real Name: " + \
                  str(self.current_barista.real_name) + " Slack Name: " + \
                  str(self.current_barista.name)

            self.humor_sent = False
            self.annoy_sent = False
            self.negative_sent = False

            # Inform them via slack that it is there turn to brew coffee
            self.slack.barista_request_for_member(Phrase.BARISTA_REQUEST_BREW_POSITIVE, self.current_barista)

            # Play the coffee is low sound
            yield self.publish('com.makeandbuild.rpi.audio.play', 'https://s3.amazonaws.com/makeandbuild/courier/audio/1.wav')

        else:
            # Check the threshold
            current_timestamp = (time.time() - self.start_timestamp)

            if self.negative_threshold < current_timestamp:
                if not self.negative_sent:
                    self.slack.barista_request_for_member(Phrase.BARISTA_REQUEST_BREW_NEGATIVE, self.current_barista)
                    self.negative_sent = True
            elif self.annoy_threshold < current_timestamp:
                if not self.annoy_sent:
                    self.slack.barista_request_for_member(Phrase.BARISTA_REQUEST_BREW_ANNOY, self.current_barista)
                    self.annoy_sent = True
            elif self.remind_humor_threshold < current_timestamp:
                if not self.humor_sent:
                    self.slack.barista_request_for_member(Phrase.BARISTA_REQUEST_BREW_HUMOR, self.current_barista)
                    self.humor_sent = True


    @wamp.subscribe(u'com.makeandbuild.coffee.brewing')
    def coffee_brewing(self):
        # Set the start timestamp to None since they started the brewing process.
        self.start_timestamp = None


    @wamp.subscribe(u'com.makeandbuild.coffee.refilled')
    def reset_countdown_timer(self):
        self.start_timestamp = None

        if not self.current_barista is None:
            self.slack.barista_request_for_member(Phrase.BARISTA_THANKS_FOR_REFILL, self.current_barista)
            self.current_barista = None