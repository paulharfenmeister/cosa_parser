import unittest
import os
import css_classes

from cosa_file import CosaHTML
from cosa_file import _used_css_classes

TEST_DIRECTORY = os.path.dirname(__file__)


class TestCosaHTML(unittest.TestCase):
    def setUp(self):
        self.test_cosa = CosaHTML(TEST_DIRECTORY + '/test_meeting.htm')

    def test_finds_all_css_classes(self):
        aklz_elem = self.test_cosa.root.find_class('body')[0]
        found_classes = set(_used_css_classes(aklz_elem))
        expected_classes = {'body', 'KopfZ1', 'KopfZ11', 'KopfZ12', }

        self.assertSetEqual(found_classes, expected_classes)

    def test_finds_correct_number_of_event_fragments(self):
        found_fragments = list(self.test_cosa.event_fragments())
        num_found_fragments = len(found_fragments)
        expected_num_found_fragments = 2

        self.assertEqual(num_found_fragments, expected_num_found_fragments)

    def test_finds_event_fragments(self):
        found_fragments = list(self.test_cosa.event_fragments())

        for (_, fragment) in found_fragments:
            self.assertGreater(len(fragment), 0)

            found_eventname = False
            for table in fragment:
                eventname = table.find_class(css_classes.EVENT_NAME[0])
                if eventname:
                    found_eventname = True

            self.assertTrue(found_eventname)

    def test_event_fragments_dont_contain_nonevent_fragments(self):
        found_fragments = self.test_cosa.event_fragments()
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
        event_fragment = list(self.test_cosa.event_fragments())[0][1]
        found_description_fragments = list(self.test_cosa.
            event_description_fragments_in_event_fragment(
            event_fragment))

        self.assertEqual(len(found_description_fragments), 2)

    def test_finds_event_results(self):
        event_fragment = list(self.test_cosa.event_fragments())[0][1]
        found_result_fragments = list(self.test_cosa.
            result_fragments_in_event_fragment(
            event_fragment
        ))

        self.assertEqual(len(found_result_fragments), 1)
