#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from random_number import Random
from random_number import RandomEnd
from encrypter import Encryption
from bid import Bid
from bid import BidEnd

decrypter = Encryption()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class Verify(webapp2.RequestHandler):
    def get(self):
        token = self.request.GET['token']

        if token:
            self.response.write(decrypter.decrypt(token))
        else:
            self.response.write('Token is missing')


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/random', Random),
                               ('/end', RandomEnd),
                               ('/verify', Verify),
                               ('/bid', Bid),
                               ('/bidend', BidEnd)], debug=True)
