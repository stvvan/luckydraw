import urllib2
import json


class Slack:

    def __init__(self):
        self.url = 'https://hooks.slack.com/services/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'

    def send(self, text):
        data = {'text': text}
        data = json.dumps(data)
        req = urllib2.Request(self.url, data, {'Content-Type': 'application/json'})
        urllib2.urlopen(req)