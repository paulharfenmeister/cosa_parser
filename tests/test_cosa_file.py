import unittest
import os
import css_classes
import sexes

from cosa_file import CosaHTML
from models import *

TEST_DIRECTORY = os.path.dirname(__file__)


class TestCosaHTML(unittest.TestCase):
    def setUp(self):
        self.test_cosa = CosaHTML(TEST_DIRECTORY + '/test_meeting.htm')

    def test_finds_all_css_classes(self):
        aklz_elem = self.test_cosa.root.find_class('body')[0]
        found_classes = set(CosaHTML._used_css_classes(aklz_elem))
        expected_classes = {'body', 'KopfZ1', 'KopfZ11', 'KopfZ12', }

        self.assertSetEqual(found_classes, expected_classes)

    def test_finds_correct_number_of_event_fragments(self):
        found_fragments = list(self.test_cosa._event_fragments())
        num_found_fragments = len(found_fragments)
        expected_num_found_fragments = 2

        self.assertEqual(num_found_fragments, expected_num_found_fragments)

    def test_finds_event_fragments(self):
        found_fragments = list(self.test_cosa._event_fragments())

        for (_, fragment) in found_fragments:
            self.assertGreater(len(fragment), 0)

            found_eventname = False
            for table in fragment:
                eventname = table.find_class(css_classes.EVENT_NAME[0])
                if eventname:
                    found_eventname = True

            self.assertTrue(found_eventname)

    def test_event_fragments_dont_contain_nonevent_fragments(self):
        found_fragments = self.test_cosa._event_fragments()
        non_event_fragment_class = 'AklZ'

        for _, fragment in found_fragments:
            elems_with_non_event_fragment_class = [
                elem.find_class(non_event_fragment_class)
                for elem in fragment]

            self.assertTrue(not any(elems_with_non_event_fragment_class))

    def test_creates_meeting(self):
        meeting = self.test_cosa.meeting()
        found_name = meeting.name
        expected_name = '42. Fischbacher Abendsportfeste'

        self.assertEqual(found_name, expected_name)

    def test_finds_event_descriptions(self):
        event_fragment = list(self.test_cosa._event_fragments())[0][1]
        found_description_fragments = list(self.test_cosa.
            _event_description_fragments_in_event_fragment(
            event_fragment))

        self.assertEqual(len(found_description_fragments), 2)

    def test_finds_event_results(self):
        event_fragment = list(self.test_cosa._event_fragments())[0][1]
        found_result_fragments = list(self.test_cosa.
            _result_fragments_in_event_fragment(
            event_fragment))

        self.assertEqual(len(found_result_fragments), 1)

    def test_builds_event_fragment(self):
        meeting = self.test_cosa.meeting()
        events = [
            CosaHTML._build_from_event_fragment(event_fragment, ageclass,
                                               meeting)
            for ageclass, event_fragment in self.test_cosa._event_fragments()]
        found_event_names = set([event.name for event in events])
        expected_event_names = {'200 m Männer', 'Stundenlauf Männer'}

        self.assertSetEqual(found_event_names, expected_event_names)

    def test_sex_from_ageclass_works(self):
        female_ageclasses = ('Frauen', 'Weibliche-Jugend-U20', 'Jugend-W15',)
        male_ageclasses = ('Manner', 'Mannliche-Jugend-U20', 'Jugend-M15',)

        for female_ageclass in female_ageclasses:
            self.assertEqual(CosaHTML._sex_from_ageclass(female_ageclass),
                             sexes.FEMALE)

        for male_ageclass in male_ageclasses:
            self.assertEqual(CosaHTML._sex_from_ageclass(male_ageclass),
                             sexes.MALE)

    def test_builds_athlete(self):
        ageclass, event_fragment = next(self.test_cosa._event_fragments())
        result_fragment = next(
            self.test_cosa._result_fragments_in_event_fragment(event_fragment))
        meeting = Meeting('Test')
        athlete = CosaHTML._build_athlete_from_result_fragment(result_fragment,
                                                              meeting,
                                                              ageclass)
        found_athlete_name = athlete.last_name
        expected_athlete_name = 'Franz'

        self.assertEqual(found_athlete_name, expected_athlete_name)
