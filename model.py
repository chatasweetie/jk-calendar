"""Class for database for JK Calendar"""
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """This is an individual user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        )
    email = db.Column(db.String(200),
                      nullable=True,
                     )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<User user_name: {}>""".format(self.email)


class Calendar(db.Model):
    """This is the individual calendar"""

    __tablename__ = "calendars"

    cal_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True,
                       )
    name = db.Column(db.String(100),
                     nullable=True
                    )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Calendar name: {}>""".format(self.name)


class Calendar_User(db.Model):
    """This is the individual relationship between a User & Calendar"""

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
                        nullable=False,)

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


class Permission(db.Model):
    """This is an individual permission level"""

    __tablename__ = "permissions"

    permission_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True,
                              )

    permission_code = db.Column(db.String(20),
                                 nullable=True,
                                 )

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Permission permission_code: {}>""".format(self.permission_code)


class Event(db.Model):
    """This is the individual event"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True,
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
                            nullable=False,
                            )
    location = db.Column(db.String(250),
                         nullable=False,
                         )
    cal_id = db.Column(db.Integer,
                       db.ForeignKey("calendars.cal_id"),
                       nullable=False,
                       )
    location_time_zone = db.Column(db.String(100),
                                   nullable=False)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Event: id: {}, title: {}>""".format(self.id,
                                                       self.title)


class Calendar_Event(db.Model):
    """This is an individual relationship between Calendars & Events"""

    __tablename__ = "calendar_events"

    cal_event_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True,
                             )
    cal_id = db.Column(db.Integer,
                       db.ForeignKey("calendars.cal_id"),
                       nullable=False,
                      )
    event_id = db.Column(db.Integer,
                            db.ForeignKey("events.event_id"),
                            nullable=False,
                            )
    permissions = db.Column(db.Integer,
                            db.ForeignKey("permissions.permission_id"),
                            nullable=False)

    event = db.relationship("Event", backref="calendar_events")
    calendar = db.relationship("Calendar", backref="calendar_events")

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Calendar_Event event_title: {} >""".format(self.event_id)

# ##########################################################################
# # Helper Functions


# def checks_user_db(user_name, user_phone):
#     """checks the db if the user is in the db and returns user object"""

#     user = User.query.filter_by(user_phone=user_phone).first()

#     if user:
#         return user

#     new_user = User(user_name=user_name, user_phone=user_phone)
#     db.session.add(new_user)
#     db.session.commit()

#     return User.query.filter_by(user_phone=user_phone).first()


# def adds_transit_request(user_inital_stop, destination_stop, agency, route,
#     route_code, arrival_time_datetime, user_db):
#     """adds a transit request to the database"""

#     now = datetime.utcnow()
#     new_transit_request = Transit_Request(inital_stop_code=user_inital_stop,
#                 destination_stop_code=destination_stop, agency=agency, route=route,
#                 route_code=route_code, arrival_time=arrival_time_datetime,
#                 start_time_stamp=now, current_stop=user_inital_stop,
#                 user_id=user_db.user_id)

#     db.session.add(new_transit_request)
#     db.session.commit()


# def list_of_is_finished_to_process():
#     """Gets all the transit_request that need to be processed (ie. is_finished = False)"""

#     request_to_process = Transit_Request.query.filter(Transit_Request.is_finished == False).all()

#     return request_to_process


# def gets_agency_db(name):
#     """returns the db object of an agency"""

#     return Agency.query.filter_by(name=name).first()


# def gets_route_db(route_code, direction=False):
#     """returns the db object of a route"""

#     if direction is False:
#         return Route.query.filter_by(route_code=route_code).first()

#     return Route.query.filter_by(route_code=route_code, direction=direction).first()


# def gets_route_id_db(route_id):
#     """returns the db object of a route"""

#     return Route.query.filter_by(route_id=route_id).first()


# def gets_stop_db(stop_id):
#     """returns the db object of a stop"""

#     return Stop.query.filter_by(stop_code=stop_id).first()


# def gets_stop_name_db(stop_name):
#     """returns the db object of a stop"""

#     return Stop.query.filter_by(name=stop_name).all()


# def update_request(request):
#     """Updates the request's information into the db"""

#     db.session.commit()


# def records_request_complete_db(request, now):
#     """Changes the transit_request is_finished to True (request is complete)"""

#     request.end_time_stamp = now
#     request.is_finished = True
#     update_request(request)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///jkcalendar")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


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
