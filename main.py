# -*- coding: utf-8 -*-
import flask

from meetup import PYLUGMeetup


app = flask.Flask(__name__)
app.config.from_object('default_settings')

try:
    app.config.from_envvar('PYTHONLV_SETTINGS')
except:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Using default settings')


meetup = PYLUGMeetup(app.config['MEETUP_KEY'])


@app.route("/")
def index():
    event = meetup.next_event()
    return flask.render_template("landing.html", event=event)


if __name__ == "__main__":
    app.run()
