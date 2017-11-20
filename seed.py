import model
from datetime import datetime

USERS = ["sally@gmail.com",
           "bill@gmail.com",
           "alice@aol.com",
           "hank@hotmail.com",
           ]

PERMISSIONS = ["view", "edit", "owner",]

STATUSES = ["awaiting response", "accepted", "declined", "edited"]

EVENTS = [{"title": "dinner",
           "start": datetime(2017, 11, 14, 15, 30),
           "end":  datetime(2017, 11, 14, 16, 30),
            },
            {"title": "Birthday!",
             "start": datetime(2017, 11, 20, 15, 30),
             "end":  datetime(2017, 11, 20, 16, 30),
            },
            {"title": "Shopping!",
             "start": datetime(2017, 11, 24, 15, 30),
             "end":  datetime(2017, 11, 24, 16, 30),
            },
            {"title": "Buy Suit!",
             "start": datetime(2017, 12, 30, 15, 30),
             "end":  datetime(2017, 12, 30, 16, 30),
            },
            {"title": "Walk River!",
             "start": datetime(2017, 11, 16, 15, 30),
             "end":  datetime(2017, 11, 16, 16, 30),
            },
            {"title": "Jesus Birthday!",
             "start": datetime(2017, 12, 25, 15, 30),
             "end":  datetime(2017, 12, 25, 16, 30),
            },
            {"title": "Code!",
             "start": datetime(2018, 11, 20, 15, 30),
             "end":  datetime(2017, 11, 20, 16, 30),
            },
            {"title": "Holiday Party!",
             "start": datetime(2017, 11, 27, 15, 30),
             "end":  datetime(2017, 11, 27, 16, 30),
            },
            {"title": "Icecream!",
             "start": datetime(2017, 11, 23, 15, 30),
             "end":  datetime(2017, 11, 23, 16, 30),
            },
            ]


def create_permissions(p_list):
    """Creates and commits permissions"""

    for p in p_list:
        permission = model.Permission(permission_code=p)

        model.db.session.add(permission)

    model.db.session.commit()


def create_users(u_list):
    """Creates and commits users to db"""

    for user in u_list:

        new_user = model.User(email=user)

        model.db.session.add(new_user)

    model.db.session.commit()



def create_cal():
    """Creates and commits calendars and associations

        Uses query to db to make the 'main/default' calendar for
        the user account.
    """

    users = model.User.query.all()
    permission = model.Permission.query.filter_by(permission_code="owner").first()

    for user in users:
        new_cal = model.Calendar(name=user.email)

        model.db.session.add(new_cal)
        model.db.session.commit()
        # commit generates id - allows us to make association.
        new_association = model.Calendar_User(cal_id=new_cal.cal_id,
                                        user_id=user.user_id,
                                        permissions=permission.permission_id,
                                        )
        model.db.session.add(new_association)

    model.db.session.commit()


def create_status(s_list):
    """Creates and commits statuses

    """

    for status in s_list:
        new_stat = model.Status(status=status)

        model.db.session.add(new_stat)

    model.db.session.commit()


def make_event(event, cal_id):

    start_week = event["start"].isocalendar()[:2]
    end_week = event["end"].isocalendar()[:2]

    return model.Event(cal_id=cal_id,
                        title=event["title"],
                        start=event["start"],
                        end=event["end"],
                        )

def create_events(e_list):
    """Creates and commits events

    """

    cals = model.Calendar.query.all()
    count = 0

    for cal in cals:

        event_1 = make_event(e_list[count], cal.cal_id)
        event_2 = make_event(e_list[count + 1], cal.cal_id)
        count += 2

        model.db.session.add_all([event_1, event_2])

    model.db.session.commit()


def create_invites():

    invite = model.Event_Invite(event_id=1,
                                status_id=1,
                                cal_id=4)
    model.db.session.add(invite)
    model.db.session.commit()


if __name__ == '__main__':

    from server import app
    import os

    print "Dropping DB"
    print "***********"
    os.system("dropdb jkcalendar")
    print "Creating DB"
    print "***********"
    os.system("createdb jkcalendar")

    model.connect_to_db(app)

    create_permissions(PERMISSIONS)
    create_users(USERS)
    create_cal()
    create_status(STATUSES)
    create_events(EVENTS)
    create_invites()
