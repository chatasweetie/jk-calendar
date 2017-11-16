from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import datetime

from model import connect_to_db

app = Flask(__name__)


@app.route("/")
def home_view():
    """Display Homepage"""

    return render_template("homepage.html")


@app.route("/week")
def week_view():
    """Display calendar in a week view"""

    # query database for calendar's events
    week_title = "November 20 - 26, 2018"
    times = []

    return render_template("week_view.html", week_title=week_title, times=times)


# app.jinja_env.filters['datetime'] = format_datetime

if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    DEBUG = "NO_DEBUG"
    PORT = 5000

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
