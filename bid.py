import webapp2
from participants import Participants
from random import randint
from slack import Slack

participants = []
prices = []
slack = Slack()

MIN = 1
MAX = 10000000

class BidStart(webapp2.RequestHandler):
    def post(self):
        user_name = self.request.POST['user_name']

        if user_name == 'steve':
            prices.append(randint(MIN, MAX))
            slack.send("Bidding round has started!")        

class Bid(webapp2.RequestHandler):
    def post(self):
        token = self.request.POST['token']

        if token == '':
            user_name = self.request.POST['user_name']
            user_id = self.request.POST['user_id']

            bid_amount = self.request.POST['text']

            if self.is_float(bid_amount) and float(bid_amount) < MAX:
                participant = Participants(user_id, user_name, float(bid_amount))

                if participant in participants:
                    participant.random_number = float(bid_amount)
                    participants[participants.index(participant)] = participant
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

            if winner is None:
                slack.send("Price is {0}. All bids are higher than price. There's no winner".format(prices[0]))
            else:
                slack.send("Price is {0}. Winning amount is: {1} and winner is: {2}. Congratulations!".format(prices[0],
                                                                                                 winner.random_number,
                                                                                                 winner.user_name),
                       True)
            del participants[:]
            del prices[:]

    @staticmethod
    def determine_winner():
        winner = None

        if participants:
            lowest = MAX - participants[0].random_number
        
            for participant in participants:
                diff = prices[0] - participant.random_number

                if diff == 0:
                    return participant

                if 0 < diff < lowest:
                    lowest = diff
                    winner = participant

        return winner


class BidClear(webapp2.RequestHandler):
    def post(self):

        user_name = self.request.POST['user_name']

        if user_name == 'steve':
            del participants[:]
            del prices[:]
            slack.send("Bidding data has been cleared.")
