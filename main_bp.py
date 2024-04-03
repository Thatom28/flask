from flask import Blueprint, render_template

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def hello_world():
    return "<h1>Hello, Sanlam🌍!</h1>"


name = "Thato"
hobbies = ["gaming", "codong", "gym", "reading"]


@main_bp.route("/profile")
def profile():
    return render_template("profile.html", name=name, hobbies=hobbies)
