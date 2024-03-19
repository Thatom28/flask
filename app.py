from flask import Flask

app = Flask(__name__)


# the home page what should we return
# this is a page
@app.route("/")
def hello_world():
    return "<h1>Hello, Sanlam!</h1>"


@app.route("/about")
def about():
    return "<h1>About page</h1>"


if __name__ == "__main__":
    app.run(debug=True)
