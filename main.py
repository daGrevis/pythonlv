import flask


app = flask.Flask(__name__)


@app.route("/")
def hello_world():
    return flask.render_template("hello_world.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
