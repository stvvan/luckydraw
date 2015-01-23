import urllib2
import json
from encrypter import Encryption


class Slack:

    def __init__(self):
        #insert slack url
        self.url = ''
        self.encrypter = Encryption()

    def send(self, text, hashing=False):
        if hashing:
            data = {'text': "{0} - Signature: {1}".format(text, self.encrypter.encrypt(text))}
        else:
            data = {'text': text}

        data = json.dumps(data)
        req = urllib2.Request(self.url, data, {'Content-Type': 'application/json'})
        urllib2.urlopen(req)


