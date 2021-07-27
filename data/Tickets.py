class Ticket:
    def __init__(self, id, event_id, user, amount):
        self.id = id
        self.event_id = event_id
        self.user = user
        self.amount = amount

    def create_from_tuple(self, t):
        return Ticket(t[0], t[1], t[2], t[3])