def striped(css_classes):
    suffices = ('g, w')
    return [css_class + suffix for css_class in css_classes for suffix in
            suffices]

# MISC
AGE_CLASS = ('AklZ',)

# MEETING
MEETING_NAME = ('KopfZ11',)

# RESULT
RESULT_ATHLETE_NAME = striped(('blENameAS', ))
RESULT_ATHLETE_BIRTHYEAR = striped(('blEJG', ))
RESULT_ATHLETE_CLUB = striped(('blEVerein', ))
RESULT_PLACE = striped(('blERang', ))
RESULT_WIND = striped(('blERangfLW', ))
RESULT_VALUE = striped(('blELeistW', ))
RESULT_UNIT = striped(('blELBez', ))
RESULT_QUALIFICATION = striped(('blEQuali', ))

# EVENT
EVENT_NAME = ('blEWettb',)
EVENT_DAY = ('blEDatum',)
EVENT_TYPE = ('blEDis',)
EVENT_DESCRIPTION = EVENT_NAME + EVENT_DAY + EVENT_TYPE


