import webapp2
from participants import Participants
from random import randint
from slack import Slack

participants = []
prices = []
slack = Slack()

MIN = 500000
MAX = 10000000


class Bid(webapp2.RequestHandler):
    def post(self):
        prices.append(randint(MIN, MAX))
        token = self.request.POST['token']

        if token == 'OA6ggjGkG47scdbZQ0BqEuD3':
            user_name = self.request.POST['user_name']
            user_id = self.request.POST['user_id']

            bid_amount = self.request.POST['text']

            if self.is_float(bid_amount) and float(bid_amount) < MAX:
                participant = Participants(user_id, user_name, float(bid_amount))

                if participant in participants:
                    participant.random_number = float(bid_amount)
                    slack.send("User {0} updates his bid to {1}".format(participant.user_name, bid_amount))
                else:
                    if any(participant.random_number == float(bid_amount) for participant in participants):
                        slack.send("@{0}, another user already bid that amount. Bid again!".format(user_name))
                    else:
                        participants.append(participant)
                        slack.send("User {0} bids {1}".format(user_name, bid_amount))

    @staticmethod
    def is_float(text):
        try:
            float(text)
            return True
        except ValueError:
            return False


class BidEnd(webapp2.RequestHandler):
    def post(self):

        user_name = self.request.POST['user_name']

        if user_name == 'steve':
            winner = self.determine_winner()
            slack.send("Price is {0}. Winning amount is: {1} and winner is: {2}".format(prices[0],
                                                                                                 winner.random_number,
                                                                                                 winner.user_name),
                       True)
            del participants[:]
            del prices[:]

    @staticmethod
    def determine_winner():
        lowest = MAX
        winner = None
        for participant in participants:
            diff = prices[0] - participant.random_number
            if 0 <= diff <= lowest:
                lowest = diff
                winner = participant

        return winner
