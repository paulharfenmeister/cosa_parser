class Meeting:
    def __init__(self, name=""):
        self.name = name
        self.days = []
        self.athletes = []
        self.events = []

    def get_or_create_day(self, date):
        found_days = [day for day in self.days if day.date == date]
        if found_days:
            return found_days[0]
        else:
            found_days = MeetingDay(self, date)
            self.days.append(found_days)
            return found_days

    def get_or_create_athlete(self, name, year_of_birth, club):
        found_athletes = [a for a in self.athletes
                          if a.name() == name and
                          a.year_of_birth == year_of_birth]
        if found_athletes:
            return found_athletes[0]
        else:
            athlete = Athlete(name, year_of_birth, club)
            self.athletes.append(athlete)
            return athlete

    def get_or_create_event(self, name, date):
        found_events = [e for e in self.events
                        if e.name == name and
                        e.day.date == date]
        if found_events:
            return found_events[0]
        else:
            event = Event(name, self.get_or_create_day(date))
            self.events.append(event)
            return event


class MeetingDay:
    def __init__(self, meeting, date):
        self.meeting = meeting
        self.date = date


class Event:
    def __init__(self, name, day):
        self.name = name
        self.day = day
        self.age_class = ""
        self.eventtype = ""
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def is_finale(self):
        finale_keywords = [
            'Finale',
        ]
        return any([keyword in self.eventtype for keyword in finale_keywords])


class Athlete:
    def __init__(self, name, year_of_birth, sex, club=""):
        self.first_name, self.last_name = self._split_name_(name)
        self.year_of_birth = year_of_birth
        self.sex = sex
        self.club = club
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def name(self):
        return "%s, %s" % (self.last_name, self.first_name)

    @staticmethod
    def _split_name_(name):
        last_name, first_name = name.split(',')
        return first_name[1:], last_name


class Result:
    def __init__(self, athlete, event, value, unit=None, wind=None, rang=None):
        self.athlete = athlete
        self.event = event
        self.value = value
        self.unit = unit
        self.wind = wind
        self.rang = rang

    def is_finale(self):
        return self.event.is_finale()
