EXCLUDE_FIELDS = ['id', 'created_at', 'updated_at', 'unit', 'session', 'year']
ADMIN_EXCLUDE_FIELDS = ['created_at', 'updated_at']


class Session(object):
    # started from 1 to make month more intiuitive
    JUL = 1
    AUG = 2
    SEP = 3
    OCT = 4
    NOV = 5
    DEC = 6
    JAN = 7
    FEB = 8
    MAR = 9
    APR = 10
    MAY = 11
    JUN = 12

    Q1 = 13
    Q2 = 14
    Q3 = 15
    Q4 = 16

    H1 = 17
    H2 = 18

    CHOICES = (
        (JUL, "Jul"),
        (AUG, "Aug"),
        (SEP, "Sep"),
        (OCT, "Oct"),
        (NOV, "Nov"),
        (DEC, "Dec"),
        (JAN, "Jan"),
        (FEB, "Feb"),
        (MAR, "Mar"),
        (APR, "Apr"),
        (MAY, "May"),
        (JUN, "Jun"),

        (Q1, "Q1"),
        (Q2, "Q2"),
        (Q3, "Q3"),
        (Q4, "Q4"),

        (H1, "H1"),
        (H2, "H2"),
    )

    @classmethod
    def get_sessions(cls, start, stop):
        return [i for i in range(start, stop)]

    @classmethod
    def get_session_list(cls, limit=12):
        session_list = []

        for choice in cls.CHOICES:
            if choice[0] <= limit:
                session_list.append(choice)

        return session_list + [(cls.Q1, "Q1"), (cls.Q2, "Q2"), (cls.Q3, "Q3"),
                               (cls.Q4, "Q4"), (cls.H1, "H1"), (cls.H2, "H2")]

    @classmethod
    def get_session_quarter(cls, session):

        if session < 4:
            return cls.get_sessions(start=1, stop=4)

        elif session < 7:
            return cls.get_sessions(start=4, stop=7)

        elif session < 10:
            return cls.get_sessions(start=7, stop=10)

        else:
            return cls.get_sessions(start=10, stop=13)

    @classmethod
    def get_session_half(cls, session):

        if session < 7:
            return cls.get_sessions(start=1, stop=7)

        else:
            return cls.get_sessions(start=7, stop=13)


class UnitType(object):

    SEMI = 0
    AUTO = 1
    TOTAL = 2

    CHOICES = (
        (SEMI, "Semi-Auto"),
        (AUTO, "Auto"),
        (TOTAL, "Total"),
    )
