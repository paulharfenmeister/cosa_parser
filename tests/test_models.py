import unittest
import datetime
from models import *


class TestMeeting(unittest.TestCase):
    def test_create_meeting(self):
        meeting = Meeting("Meeting")
        self.assertFalse(meeting.days)
        self.assertFalse(meeting.events)
        self.assertFalse(meeting.athlets)

    def test_get_or_create_day(self):
        meeting = Meeting("Meeting")
        date = datetime.date(2015, 8, 24)
        day = meeting.get_or_create_day(date)
        self.assertIn(meeting.get_or_create_day(date), meeting.days)
        self.assertEqual(day, meeting.get_or_create_day(date))

    def test_get_or_create_athlet(self):
        meeting = Meeting("Meeting")
        athlet = meeting.get_or_create_athlet("Bolt, Usain", 1986, "Club")
        self.assertIn(athlet, meeting.athlets)
        self.assertEqual(athlet, meeting.get_or_create_athlet(
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
        athlet = meeting.get_or_create_athlet("Bolt, Usain", 1986, "Club")
        self.assertEqual(athlet, meeting.get_or_create_athlet(
            "Bolt, Usain", 1986, "Club"))

    def test_add_result(self):
        meeting = Meeting("Meeting")
        athlet = meeting.get_or_create_athlet("Bolt, Usain", 1986, "Club")
        date = datetime.date(2015, 8, 24)
        event = meeting.get_or_create_event("100 m U20 Männer", date)
        r = Result(athlet, event, 9.58, 's', '+1,3', 1)
        athlet.add_result(r)
        self.assertIn(r, athlet.results)

    def test_split_name(self):
        last_name = "Lastname"
        first_name = "Firstname"
        athlet_name = "%s, %s" % (last_name, first_name)
        self.assertEqual((first_name, last_name),
                         Athlet.__split_name__(athlet_name))
        last_name = "Last Name"
        first_name = "First Name"
        athlet_name = "%s, %s" % (last_name, first_name)
        self.assertEqual((first_name, last_name),
                         Athlet.__split_name__(athlet_name))


class TestResult(unittest.TestCase):
    def test_result_is_final(self):
        meeting = Meeting("Meeting")
        date = datetime.date(2015, 8, 24)
        event = meeting.get_or_create_event("100 m U20 Männer", date)
        athlet = meeting.get_or_create_athlet("Bolt, Usain", 1986, "Club")
        r = Result(athlet, event, 9.58, 's', '+1,3', 1)
        self.assertEqual(r.is_final(), event.is_final)
