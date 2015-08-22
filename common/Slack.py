import json
import requests
from PhraseEngine import PhraseEngine, Phrase

class SlackMember():

    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.real_name = data.get("real_name")
        self.is_bot = data.get("is_bot")
        self.first_name = data.get("profile").get("first_name")
        self.last_name = data.get("profile").get("last_name")
        self.email = data.get("profile").get("email")

class Slack():

    coffee_bot_webhook = "https://makeandbuild.slack.com/services/hooks/incoming-webhook?token=iOIa6CL9xEGuYgUbl7m7kOlq"
    mnb_token = "xoxp-2549074609-2562050856-2806124350-53c681"
    coffee_status_url = "<http://courier.makeandbuildatl.com:9015|Coffee Status"
    members = []
    phrase_engine = PhraseEngine()

    def __init__(self):
        print "Creating Slack instance"
        self.members = self.get_members()

    def get_members(self):
        member_list_url = "https://slack.com/api/users.list?token={}&pretty=1".format(self.mnb_token)
        json_data = json.loads(requests.get(member_list_url).content)

        if not json_data["ok"]:
            print "Response is NOT ok"
            return None

        cache = []
        for member in json_data['members']:
            cache.append(SlackMember(member))

        print "Cached " + str(len(cache)) + " Slack members"

        return cache

    def barista_request_for_member(self, phrase_type, slack_member):
        msg = {"text": self.phrase_engine.generate_phrase(phrase_type, slack_member), "channel": "#testing123"}
        self.post_msg_to_slack(msg)

    def post_msg_to_slack(self, msg):
        payload = json.dumps({"text": str(msg["text"]),
                              "channel": str(msg["channel"]),
                              "username": "Coffee Bot", "icon_emoji": ":coffee:"})
        requests.post(self.coffee_bot_webhook, data=payload)

if __name__ == '__main__':
    slack = Slack()
    slack.barista_request_for_member(Phrase.BARISTA_REQUEST_BREW_POSITIVE, slack.members[8])