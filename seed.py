import model

USERS = ["sally@gmail.com",
           "bill@gmail.com",
           "alice@aol.com",
           "hank@hotmail.com",
           ]

PERMISSIONS = ["view", "edit", "owner",]


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


if __name__ == '__main__':

    from server import app

    model.connect_to_db(app)

    create_permissions(PERMISSIONS)
    create_users(USERS)
    create_cal()
