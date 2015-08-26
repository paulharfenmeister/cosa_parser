import lxml.html
import css_classes

from resources import CosaResource
from functools import reduce
from models import *
from datetime import date


class CosaHTML(CosaResource):
    def meeting(self):
        fragment = self.meeting_fragment()
        name = fragment.find_class(css_classes.MEETING_NAME[0])[0].text
        meeting = Meeting(name=name)
        return meeting

    def athlete(self, first_name=None, last_name=None, year_of_birth=None):
        pass

    def __init__(self, filename):
        self.doc = lxml.html.parse(filename)
        self.root = self.doc.getroot()
        self.body = self.root.findall('./body')[0]

    def build(self):
        pass

    def event_fragments(self):
        fragment = []
        ageclass = None
        reached_events = False

        for elem in self.body:
            found_ageclasses = CosaHTML._find_classes(elem,
                                                      css_classes.AGE_CLASS)
            if found_ageclasses:
                ageclass = found_ageclasses[0]

            found_eventnames = CosaHTML._find_classes(elem,
                                                      css_classes.EVENT_NAME)
            if found_eventnames:
                reached_events = True
                if fragment:
                    event_fragment = fragment[:]
                    fragment = [elem]
                    yield (
                        ageclass,
                        CosaHTML._filter_non_event_fragments(event_fragment))
                else:
                    fragment = [elem]
            elif reached_events and elem.tag.lower() == 'table':
                fragment.append(elem)

        yield (ageclass, CosaHTML._filter_non_event_fragments(fragment))

    def meeting_fragment(self):
        return self.body.getchildren()[0]

    @staticmethod
    def build_from_event_fragment(event_fragment, age_class):
        description_fragment = CosaHTML.event_description_fragments_in_event_fragment(
            event_fragment)
        result_fragments = CosaHTML.result_fragments_in_event_fragment(
            event_fragment)

        event_name = CosaHTML._get_text(description_fragment,
                                        css_classes.EVENT_NAME[0])
        event_date = CosaHTML._get_text(description_fragment,
                                        css_classes.EVENT_DAY[0])
        event_type = CosaHTML._get_text(description_fragment,
                                        css_classes.EVENT_TYPE[0])

        event = Event(event_name, CosaHTML._str_to_date(event_date))
        results = [CosaHTML.build_from_result_fragment(result_fragment, event)
                   for result_fragment in result_fragments]

        event.eventtype = event_type
        event.ak = age_class
        event.results = results

        return event

    @staticmethod
    def build_from_result_fragment(result_fragment, event):
        pass

    @staticmethod
    def event_description_fragments_in_event_fragment(event_fragment):
        for fragment in event_fragment:
            if CosaHTML._find_classes(fragment, css_classes.EVENT_DESCRIPTION):
                yield fragment

    @staticmethod
    def result_fragments_in_event_fragment(event_fragment):
        for fragment in event_fragment:
            if CosaHTML._find_classes(fragment,
                                      css_classes.RESULT_ATHLETE_NAME):
                yield fragment

    @staticmethod
    def _used_css_classes(elem):
        children = elem.getchildren()
        found_classes = [elem.attrib['class']] if 'class' in elem.attrib else []

        if not children:
            return found_classes

        else:
            return found_classes + reduce(lambda a, b: a + b,
                                          [CosaHTML._used_css_classes(child) for
                                           child in children])

    @staticmethod
    def _filter_non_event_fragments(fragments):
        event_fragments = [fragment for fragment in fragments if
                           any(['blE' in css_class
                                for css_class in
                                CosaHTML._used_css_classes(fragment)])]
        return event_fragments

    @staticmethod
    def _find_classes(fragment, classes):
        found_elems = reduce(lambda a, b: a + b,
                             [fragment.find_class(css_class) for css_class in
                              classes])
        return found_elems

    @staticmethod
    def _get_text(fragment, css_class):
        elems = reduce(lambda a, b: a + b,
                       [fragment_part.find_class(css_class) for fragment_part in
                        fragment])
        texts = [elem.text for elem in elems]
        assert len(texts) <= 1, 'Selection should be unique.'
        return texts[0] if texts else ""

    @staticmethod
    def _str_to_date(string):
        split = string.split('.')
        return date(int(split[2]), int(split[1]), int(split[0]))
