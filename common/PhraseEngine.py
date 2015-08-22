#This class serves as a engine to generates phrases that will be sent out to social media, email, audio, and other hooks
import random

class Phrase():

    BARISTA_REQUEST_BREW_POSITIVE = 0
    BARISTA_REQUEST_BREW_HUMOR = 1
    BARISTA_REQUEST_BREW_ANNOY = 2
    BARISTA_REQUEST_BREW_NEGATIVE = 3
    BARISTA_THANKS_FOR_REFILL = 4

    def __init__(self, aggression, phrase):
        self.aggression = aggression
        self.phrase = phrase

class PhraseEngine():

    #Holds the phrases known by the PhraseEngine
    phrases = {}

    def __init__(self):
        print "Created instance of the PhraseEngine()"

        barista_request_positive = []
        barista_request_positive.append(Phrase(Phrase.BARISTA_REQUEST_BREW_POSITIVE, "@{} its your turn to play barista"))
        barista_request_positive.append(Phrase(Phrase.BARISTA_REQUEST_BREW_POSITIVE, "@{} could you please brew us some more coffee? We are running low"))
        barista_request_positive.append(Phrase(Phrase.BARISTA_REQUEST_BREW_POSITIVE, "@{} coffee is low can you brew some more?"))
        self.phrases[Phrase.BARISTA_REQUEST_BREW_POSITIVE] = barista_request_positive

        barista_request_humor = []
        barista_request_humor.append(Phrase(Phrase.BARISTA_REQUEST_BREW_HUMOR, "Just a reminder @{} you still haven't brewed more coffee"))
        barista_request_humor.append(Phrase(Phrase.BARISTA_REQUEST_BREW_HUMOR, "@{} did you forget it was your turn to brew more coffee?"))
        barista_request_humor.append(Phrase(Phrase.BARISTA_REQUEST_BREW_HUMOR, "Dude I know your busy @{} but it won't take a few minutes to step away and make some more coffee for everyone"))
        self.phrases[Phrase.BARISTA_REQUEST_BREW_HUMOR] = barista_request_humor

        barista_request_annoy = []
        barista_request_annoy.append(Phrase(Phrase.BARISTA_REQUEST_BREW_ANNOY, "makebot gif me barista"))
        barista_request_annoy.append(Phrase(Phrase.BARISTA_REQUEST_BREW_ANNOY, "@{} your 5 minutes away from a red card and 100 spam emails if you don't brew more coffee!"))
        barista_request_annoy.append(Phrase(Phrase.BARISTA_REQUEST_BREW_ANNOY, "@{} even the 17 year old at starbucks can brew coffee. Get off your ass and go make some!"))
        self.phrases[Phrase.BARISTA_REQUEST_BREW_ANNOY] = barista_request_annoy

        barista_request_negative = []
        barista_request_negative.append(Phrase(Phrase.BARISTA_REQUEST_BREW_NEGATIVE, "@{} what kind of asshole won't even make coffee for his co workers?"))
        # barista_request_negative.append(Phrase(Phrase.BARISTA_REQUEST_BREW_NEGATIVE, ""))
        # barista_request_negative.append(Phrase(Phrase.BARISTA_REQUEST_BREW_NEGATIVE, ""))
        self.phrases[Phrase.BARISTA_REQUEST_BREW_NEGATIVE] = barista_request_negative

        barista_thanks_refill = []
        barista_thanks_refill.append(Phrase(Phrase.BARISTA_THANKS_FOR_REFILL, "@{} you the man thanks for making some more coffee!"))
        barista_thanks_refill.append(Phrase(Phrase.BARISTA_THANKS_FOR_REFILL, "makebot give @{} 10 points"))
        barista_thanks_refill.append(Phrase(Phrase.BARISTA_THANKS_FOR_REFILL, "@{} your mom would be proud!"))
        self.phrases[Phrase.BARISTA_THANKS_FOR_REFILL] = barista_thanks_refill

    def generate_phrase(self, phrase_type, slack_member):
        inner_phrases = self.phrases[phrase_type]
        print inner_phrases
        randint = random.randint(0, len(inner_phrases) - 1)
        ph = str(inner_phrases[randint].phrase.format(slack_member.name))
        print "Random Phrase: " + str(ph)
        return ph

if __name__ == '__main__':
    pe = PhraseEngine()