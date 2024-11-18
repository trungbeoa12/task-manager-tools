class Calendar:
    def __init__(self):
        self.events = {}

    def add_event(self, date, task):
        if date not in self.events:
            self.events[date] = []
        self.events[date].append(task)

    def get_events_by_date(self, date):
        return self.events.get(date, [])

