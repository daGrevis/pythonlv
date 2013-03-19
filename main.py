# -*- coding: utf-8 -*-
import flask

from meetup import PYLUGMeetup


app = flask.Flask(__name__)


@app.route("/")
def index():
    event = meetup.next_event()
    return flask.render_template("landing.html", event=event)


def _parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--meetup-key')
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    meetup = PYLUGMeetup(args.meetup_key or '3b6a2c23416b587c54452c2f75263830')
    app.debug = True
    app.run()
