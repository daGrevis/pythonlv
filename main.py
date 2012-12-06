import flask


app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("landing.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
