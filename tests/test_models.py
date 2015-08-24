import unittest
import datetime
from models import *


class TestMeeting(unittest.TestCase):
    def test_create_meeting(self):
        meeting = Meeting("Meeting")
        self.assertFalse(meeting.days)
        self.assertFalse(meeting.athlets)

    def test_get_or_create_day(self):
        meeting = Meeting("Meeting")
        day = datetime.date(2015, 8, 24)
        meeting.get_or_create_day(day)
        self.assertIn(meeting.get_or_create_day(day), meeting.days)

    def test_get_or_create_athlet(self):
        meeting = Meeting("Meeting")
        athlet = meeting.get_or_create_athlet("Bolt, Usain", 1987, "Club")
        self.assertEqual(athlet, meeting.get_or_create_athlet(
            "Bolt, Usain", 1987, "Club"))
