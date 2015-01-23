from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 32
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)


class Encryption:

    def __init__(self):
        #insert secret key here
        self.cipher = AES.new('1234567876543211')

    def encrypt(self, text):
        return EncodeAES(self.cipher, text)

    def decrypt(self, text):
        return DecodeAES(self.cipher, text)