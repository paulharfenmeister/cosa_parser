import lxml.html
import css_classes
import regexps
import re
import sexes

from resources import CosaResource
from functools import reduce
from models import *
from datetime import date
from operator import xor


class CosaHTML(CosaResource):
    def meeting(self):
        fragment = self._meeting_fragment()
        name = fragment.find_class(css_classes.MEETING_NAME[0])[0].text
        meeting = Meeting(name=name)
        return meeting

    def athlete(self, first_name=None, last_name=None, year_of_birth=None):
        pass

    def __init__(self, filename):
        self.doc = lxml.html.parse(filename)
        self.root = self.doc.getroot()
        self.body = self.root.findall('./body')[0]

    def _build(self):
        pass

    def _event_fragments(self):
        fragment = []
        ageclass = None
        reached_events = False

        for elem in self.body:
            found_ageclasses = CosaHTML._find_classes(elem,
                                                      css_classes.AGE_CLASS)
            if found_ageclasses:
                ageclass = found_ageclasses[0].findall('./a')[0].attrib['name']

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

    def _meeting_fragment(self):
        return self.body.getchildren()[0]

    @staticmethod
    def _build_from_event_fragment(event_fragment, age_class, meeting):
        description_fragment = next(
            CosaHTML._event_description_fragments_in_event_fragment(
                event_fragment))
        result_fragments = next(CosaHTML._result_fragments_in_event_fragment(
            event_fragment))

        event_name = CosaHTML._get_text(description_fragment,
                                        css_classes.EVENT_NAME)
        event_date = CosaHTML._get_text(description_fragment,
                                        css_classes.EVENT_DAY)
        event_type = CosaHTML._get_text(description_fragment,
                                        css_classes.EVENT_TYPE)

        event = Event(event_name, CosaHTML._str_to_date(event_date))
        results = [CosaHTML._build_from_result_fragment(result_fragment, meeting,
                                                       age_class)
                   for result_fragment in result_fragments]

        event.eventtype = event_type
        event.ak = age_class
        event.results = results

        return event

    @staticmethod
    def _build_from_result_fragment(result_fragment, meeting, ageclass):
        pass

    @staticmethod
    def _build_athlete_from_result_fragment(result_fragment, meeting, ageclass):
        result_text = lambda css_class: CosaHTML._get_text(result_fragment,
                                                           css_class)
        athlete_name = result_text(css_classes.RESULT_ATHLETE_NAME)
        athlete_birthyear = result_text(css_classes.RESULT_ATHLETE_BIRTHYEAR)
        athlete_club = result_text(css_classes.RESULT_ATHLETE_CLUB)
        athlete_sex = CosaHTML._sex_from_ageclass(ageclass)

        athlete = meeting.get_or_create_athlete(athlete_name, athlete_birthyear,
                                                athlete_club)
        athlete.sex = athlete_sex

        return athlete

    @staticmethod
    def _event_description_fragments_in_event_fragment(event_fragment):
        for fragment in event_fragment:
            if CosaHTML._find_classes(fragment, css_classes.EVENT_DESCRIPTION):
                yield fragment

    @staticmethod
    def _result_fragments_in_event_fragment(event_fragment):
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
    def _get_text(fragment, css_classes):
        elems = reduce(lambda a, b: a + b,
                       [CosaHTML._find_classes(fragment_part, css_classes) for
                        fragment_part in
                        fragment])
        texts = [elem.text for elem in elems]
        assert len(texts) <= 1, 'Selection should be unique.'
        return texts[0] if texts else ""

    @staticmethod
    def _str_to_date(string):
        split = string.split('.')
        return date(int(split[2]), int(split[1]), int(split[0]))

    @staticmethod
    def _sex_from_ageclass(ageclass):
        is_male = any([re.match(male_re, ageclass)
                       for male_re in regexps.MALE_AGECLASS])
        is_female = any([re.match(male_re, ageclass)
                         for male_re in regexps.FEMALE_AGECLASS])

        assert xor(is_female, is_male), 'Age class must determine sex.'

        return sexes.FEMALE if is_female else sexes.MALE
