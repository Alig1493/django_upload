EXCLUDE_FIELDS = ['id', 'created_at', 'updated_at', 'unit', 'session', 'year']
ADMIN_EXCLUDE_FIELDS = ['created_at', 'updated_at']


class Session(object):
    # started from 1 to make month more intiuitive
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12

    Q1 = 13
    Q2 = 14
    Q3 = 15
    Q4 = 16

    H1 = 17
    H2 = 18

    CHOICES = (
        (JAN, "Jan"),
        (FEB, "Feb"),
        (MAR, "Mar"),
        (APR, "Apr"),
        (MAY, "May"),
        (JUN, "Jun"),
        (JUL, "Jul"),
        (AUG, "Aug"),
        (SEP, "Sep"),
        (OCT, "Oct"),
        (NOV, "Nov"),
        (DEC, "Dec"),

        (Q1, "Q1"),
        (Q2, "Q2"),
        (Q3, "Q3"),
        (Q4, "Q4"),

        (H1, "H1"),
        (H2, "H2"),
    )

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
            return [cls.JAN, cls.FEB, cls.MAR]

        elif session < 7:
            return [cls.APR, cls.MAY, cls.JUN]

        elif session < 10:
            return [cls.JUL, cls.AUG, cls.SEP]

        else:
            return [cls.OCT, cls.NOV, cls.DEC]

    @classmethod
    def get_session_half(cls, session):

        if session < 7:
            return [cls.JAN, cls.FEB, cls.MAR, cls.APR, cls.MAY, cls.JUN]

        else:
            return [cls.JUL, cls.AUG, cls.SEP, cls.OCT, cls.NOV, cls.DEC]


class UnitType(object):

    SEMI = 0
    AUTO = 1
    TOTAL = 2

    CHOICES = (
        (SEMI, "Semi-Auto"),
        (AUTO, "Auto"),
        (TOTAL, "Total"),
    )
