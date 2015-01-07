import urllib2
import json
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 32
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
#insert secret key here
cipher = AES.new('***')


class Slack:

    def __init__(self):
        #insert slack url
        self.url = '****'

    def send(self, text, hashing=False):
        if hashing:
            data = {'text': "{0} - Signature: {1}".format(text, EncodeAES(cipher, text))}
        else:
            data = {'text': text}

        data = json.dumps(data)
        req = urllib2.Request(self.url, data, {'Content-Type': 'application/json'})
        urllib2.urlopen(req)

    def verify(self, token):
        return DecodeAES(cipher, token)

