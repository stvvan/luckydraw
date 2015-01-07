class Participants(object):

    def __init__(self, user_id, user_name, random_number):
        self.user_id = user_id
        self.user_name = user_name
        self.random_number = random_number

    def __eq__(self, other):
        return self.user_id == other.user_id
