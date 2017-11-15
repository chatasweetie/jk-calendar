"""Class for database for JK Calendar"""
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from server import app

db = SQLAlchemy()

class Permission(db.Model):
    """An individual permission level"""

    __tablename__ = "permissions"

    permission_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True,
                              )

    permission_code = db.Column(db.String(20),
                                nullable=False,
                                unique=True,
                                )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Permission permission_code: {}>""".format(self.permission_code)


class User(db.Model):
    """An individual user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        )
    email = db.Column(db.String(254),
                      nullable=False,
                      unique=True,
                     )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<User user_name: {}>""".format(self.email)


class Calendar(db.Model):
    """An individual calendar"""

    __tablename__ = "calendars"

    cal_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True,
                       )
    name = db.Column(db.String(100),
                     nullable=False
                    )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Calendar name: {}>""".format(self.name)


class Calendar_User(db.Model):
    """The individual relationship between a User & Calendar"""

    __tablename__ = "calendar_users"

    cal_user_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True,
                            )

    cal_id = db.Column(db.Integer,
                       db.ForeignKey("calendars.cal_id"),
                       nullable=False,
                       )

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False,
                        )

    permissions = db.Column(db.Integer,
                            db.ForeignKey("permissions.permission_id"),
                            nullable=False,
                            )

    user = db.relationship("User",
                           backref="calendar_users",
                          )
    calendar = db.relationship("Calendar",
                               backref="calendar_users",
                              )


    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Calendar_User cal_id: {} user_id: {}>""".format(self.cal_id,
                                                                   self, user_id
                                                                   )


class Event(db.Model):
    """An individual event"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True,
                         )

    cal_id = db.Column(db.Integer,
                        db.ForeignKey("calendars.cal_id"),
                        nullable=False,
                        )
    start = db.Column(db.DateTime,
                      default=datetime.utcnow,
                      )
    end = db.Column(db.DateTime,
                    default=datetime.utcnow,
                    )
    title = db.Column(db.String(100),
                      nullable=False,
                      )
    description = db.Column(db.String(500),
                            nullable=True,
                            )
    location = db.Column(db.String(250),
                         nullable=True,
                         )

    location_time_zone = db.Column(db.String(100),
                                   nullable=True)

    invites = db.relationship("Event_Invite", backref="event")


    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Event: id: {}, title: {}>""".format(self.id,
                                                       self.title)


class Status(db.Model):
    """An individual status"""

    __tablename__ = "status"

    status_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True,
                          )
    status = db.Column(db.String(25),
                        unique=True,
                        nullable=False,
                        )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Status: status_id: {}, status: {}>""".format(self.status_id,
                                                                self.status)

class Event_Invite(db.Model):
    """An individual invite"""

    __tablename__ = "invites"

    invite_id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                  )
    event_id = db.Column(db.Integer,
                         db.ForeignKey("events.event_id"),
                         nullable=False,
                        )
    status_id = db.Column(db.Integer,
                          db.ForeignKey("status.status_id"),
                          nullable=True,
                          default=1
                          )
    # id of invitee.
    cal_id = db.Column(db.Integer,
                       db.ForeignKey("calendars.cal_id"),
                       nullable=False,
                            )
    time_created = db.Column(db.DateTime(timezone=True),
                                   server_default=db.func.now(),
                                   )
    time_deleted = db.Column(db.DateTime(timezone=True),
                                   onupdate=db.func.now(),
                                  )



################################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///jkcalendar")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)
    db.create_all()


# if __name__ == "__main__":
#     """will connect to the db"""
#     import os
#     os.system("dropdb jkcalendar")
#     print "Dropped DB"
#     os.system("createdb jkcalendar")
#     print "created DB"
#     # db.create_all()
#
#     from server import app
#     connect_to_db(app)
#     db.create_all()
#     print "Connected to DB."
