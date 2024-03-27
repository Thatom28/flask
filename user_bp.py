from flask import Blueprint, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import uuid
import os
from app import User, db

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/login", methods=["POST", "GET"])
def login():
    users = User.query.all()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            user = [
                user
                for user in users
                if user.username == username and user.password == password
            ]
            return render_template("welcome_page.html", user=user)
        except Exception as e:
            return render_template("login.html", error="Invalid username or password")
            # return f"<h1>Error happend {str(e)}</h1>", 500
    else:
        return render_template("login.html")


# @user_bp.route("/signup")  # HOF
# def signup():
#     return render_template("signup.html")


# create user when they sign up
@user_bp.route("/signup", methods=["POST", "GET"])
def create_user():
    users = User.query.all()
    if request.method == "POST":
        user = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
        }
        existing_user = any(user.username == users.username for user in users)
        if existing_user:
            return render_template("login.html")
        else:
            new_user = User(**data)
            try:
                db.session.add(new_user)
                db.session.commit()
                return f"<h1>{data['username']} user successfully</h1>"
            except Exception as e:
                db.session.rollback()
                return f"<h1>Error happend {str(e)}</h1>", 500
    else:
        return render_template("signup.html")
