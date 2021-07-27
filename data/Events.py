class Event:
    def __init__(self, id, event, date, time, location, places):
        self.id = id
        self.event = event
        self.date = date
        self.time = time
        self.location = location
        self.places = places

    @staticmethod
    def create_from_tuple(t):
        return Event(t[0], t[1], t[2], t[3], t[4], t[5])
