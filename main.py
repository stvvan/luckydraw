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
from participants import Participants
from random import randint
from slack import Slack

participants = []
random_numbers = []
slack = Slack()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class Random(webapp2.RequestHandler):
    def post(self):
        token = self.request.POST['token']

        if token == 'MWy79kmxOFunjxrcDMNt1y6a':
            user_name = self.request.POST['user_name']

            user_id = self.request.POST['user_id']

            random_number = randint(0, 100)
            while random_number in random_numbers:
                random_number = randint(0, 100)

            random_numbers.append(random_number)

            participant = Participants(user_id, user_name, random_number)

            if participant not in participants:
                participants.append(participant)
                slack.send("User {0} is assigned this number: {1}".format(user_name, random_number))


class RandomEnd(webapp2.RequestHandler):
    def post(self):

        user_name = self.request.POST['user_name']

        if user_name == 'steve':
            random_index = randint(0, len(participants) - 1)
            winner = participants[random_index]

            slack.send("Winner is: {0}, winning number is: {1}".format(winner.user_name, winner.random_number))

            del participants[:]
            del random_numbers[:]


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/random', Random),
                               ('/end', RandomEnd)], debug=True)
