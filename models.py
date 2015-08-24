class Meeting:
    def __init__(self, name=""):
        self.name = name
        self.days = []
        self.athlets = []
        self.events = []

    def get_or_create_day(self, date):
        day = [day for day in self.days if day.date == date]
        if day:
            return day[0]
        else:
            day = MeetingDay(self, date)
            self.days.append(day)
            return day

    def get_or_create_athlet(self, name, year_of_birth, club):
        is_already_athlet = [a for a in self.athlets
                             if a.name() == name and
                             a.year_of_birth == year_of_birth]
        if is_already_athlet:
            return is_already_athlet[0]
        else:
            athlet = Athlet(name, year_of_birth, club)
            self.athlets.append(athlet)
            return athlet

    def get_or_create_event(self, name, date):
        is_already_event = [e for e in self.events
                            if e.name == name and
                            e.day.date == date]
        if is_already_event:
            return is_already_event[0]
        else:
            event = Event(name, self.get_or_create_day(date))
            self.events.append(event)
            return event


class MeetingDay:
    def __init__(self, meeting, date):
        self.meeting = meeting
        self.date = date


class Event:
    def __init__(self, name, day, is_final=True):
        self.name = name
        self.day = day
        self.ak = ""
        self.eventtype = ""
        self.is_final = is_final
        self.results = []

    def add_result(self, result):
        self.results.append(result)


class Athlet:
    def __init__(self, name, year_of_birth, sex, club=""):
        self.first_name, self.last_name = self.__split_name__(name)
        self.year_of_birth = year_of_birth
        self.sex = sex
        self.club = club
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def name(self):
        return "%s, %s" % (self.last_name, self.first_name)

    @staticmethod
    def __split_name__(name):
        last_name, first_name = name.split(',')
        return first_name[1:], last_name


class Result:
    def __init__(self, athlet, event, value, unit=None, wind=None, rang=None):
        self.athlet = athlet
        self.event = event
        self.value = value
        self.unit = unit
        self.wind = wind
        self.rang = rang

    def is_final(self):
        return self.event.is_final