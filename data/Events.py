class Event:
    def __init__(self, id=-1, event="", date="", time="", location="", places=0):
        self.id = id
        self.event = event
        self.date = date
        self.time = time
        self.location = location
        self.places = places

    @staticmethod
    def create_from_tuple(t):
        return Event(t[0], t[1], t[2], t[3], t[4], t[5])

    def to_string(self):
        return str(self.id) + " " + self.event + " " + self.date + " " + self.time + " " + self.location + " " + str(self.places)
