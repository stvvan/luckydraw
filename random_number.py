import webapp2
from participants import Participants
from random import randint
from slack import Slack

participants = []
random_numbers = []
slack = Slack()

MIN = 1000
MAX = 9999


class Random(webapp2.RequestHandler):
    def post(self):
        token = self.request.POST['token']

        if token == 'MWy79kmxOFunjxrcDMNt1y6a':
            user_name = self.request.POST['user_name']

            user_id = self.request.POST['user_id']

            random_number = randint(MIN, MAX)
            while random_number in random_numbers:
                random_number = randint(MIN, MAX)

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

            slack.send("Winner is: {0}, winning number is: {1}".format(winner.user_name, winner.random_number), True)

            del participants[:]
            del random_numbers[:]
