import unittest
import datetime
from models import *


class TestMeeting(unittest.TestCase):
    def test_create_meeting(self):
        meeting = Meeting("Meeting")
        self.assertFalse(meeting.days)
        self.assertFalse(meeting.events)
        self.assertFalse(meeting.athletes)

    def test_get_or_create_day(self):
        meeting = Meeting("Meeting")
        date = datetime.date(2015, 8, 24)
        day = meeting.get_or_create_day(date)
        self.assertIn(meeting.get_or_create_day(date), meeting.days)
        self.assertEqual(day, meeting.get_or_create_day(date))

    def test_get_or_create_athlet(self):
        meeting = Meeting("Meeting")
        athlet = meeting.get_or_create_athlete("Bolt, Usain", 1986, "Club")
        self.assertIn(athlet, meeting.athletes)
        self.assertEqual(athlet, meeting.get_or_create_athlete(
            "Bolt, Usain", 1986, "Club"))

    def test_get_or_create_event(self):
        meeting = Meeting("Meeting")
        date = datetime.date(2015, 8, 24)
        self.assertFalse(meeting.events)
        event = meeting.get_or_create_event("100 m U20 Männer", date)
        self.assertIn(event, meeting.events)
        same_event = meeting.get_or_create_event("100 m U20 Männer", date)
        self.assertEqual(event, same_event)
        self.assertEqual(event.day, same_event.day)


class TestAthlet(unittest.TestCase):
    def test_create_athlet(self):
        meeting = Meeting("Meeting")
        athlet = meeting.get_or_create_athlete("Bolt, Usain", 1986, "Club")
        self.assertEqual(athlet, meeting.get_or_create_athlete(
            "Bolt, Usain", 1986, "Club"))

    def test_split_name(self):
        last_name = "Lastname"
        first_name = "Firstname"
        athlete_name = "%s, %s" % (last_name, first_name)
        self.assertEqual((first_name, last_name),
                         Athlete._split_name_(athlete_name))
        last_name = "Last Name"
        first_name = "First Name"
        athlete_name = "%s, %s" % (last_name, first_name)
        self.assertEqual((first_name, last_name),
                         Athlete._split_name_(athlete_name))


class TestEvent(unittest.TestCase):
    def test_create_event(self):
        meeting = Meeting("Meeting")
        date = datetime.date(2015, 8, 24)
        event = meeting.get_or_create_event("100 m U20 Männer", date)
        self.assertEqual(event, meeting.get_or_create_event(
            "100 m U20 Männer", date))

    def test_add_result(self):
        meeting = Meeting("Meeting")
        date = datetime.date(2015, 8, 24)
        event = meeting.get_or_create_event("100 m U20 Männer", date)
        athlete = meeting.get_or_create_athlete("Bolt, Usain", 1986, "Club")
        r = Result(athlete, 9.58, unit='s', wind='+1,3', place=1)
        self.assertFalse(event.results)
        event.add_result(r)
        self.assertIn(r, event.results)


class TestAttempt(unittest.TestCase):
    def test_create_attempt(self):
        meeting = Meeting("Meeting")
        athlete = meeting.get_or_create_athlete("Mustermann, Max", 1986, "Club")
        r = Result(athlete, 1.45, unit='m')
        a1, a2, a3 = Attempt(1, 'x'), Attempt(1, 'x'), Attempt(1, 'o')
        r.attempts.append(a1)
        r.attempts.append(a2)
        r.attempts.append(a3)
        self.assertEqual(len(r.attempts), 3)
        self.assertEqual(r.attempts, [a1, a2, a3])
