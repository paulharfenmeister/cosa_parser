import lxml.html
import css_classes

from resources import CosaResource
from functools import reduce


def _used_css_classes(elem):
    children = elem.getchildren()
    found_classes = [elem.attrib['class']] if 'class' in elem.attrib else []

    if not children:
        return found_classes

    else:
        return found_classes + reduce(lambda a, b: a + b, [_used_css_classes(child) for child in children])


def _filter_non_event_fragments(fragments):
    event_fragments = [fragment for fragment in fragments if any(['blE' in css_class
                                                                  for css_class in _used_css_classes(fragment)])]
    return event_fragments


class CosaHTML(CosaResource):

    def __init__(self, filename):
        self.doc = lxml.html.parse(filename)
        self.root = self.doc.getroot()
        self.body = self.root.findall('./body')[0]

    def build(self):
        skip_to_first_event = True

    def event_fragments(self):
        fragment = []
        ageclass = None
        reached_events = False
        event_fragment = None

        for elem in self.body:
            found_ageclasses = elem.find_class(css_classes.AGE_CLASS[0])
            if found_ageclasses:
                ageclass = found_ageclasses[0]

            found_eventnames = elem.find_class(css_classes.EVENT_NAME[0])
            if found_eventnames:
                reached_events = True
                if fragment:
                    event_fragment = fragment[:]
                    fragment = [elem]
                    yield (ageclass, _filter_non_event_fragments(event_fragment))
                else:
                    fragment = [elem]
            elif reached_events and elem.tag.lower() == 'table':
                fragment.append(elem)

        yield(ageclass, _filter_non_event_fragments(fragment))
