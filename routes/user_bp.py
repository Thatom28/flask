from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.users import User
from extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import login_user, login_required
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user_bp", __name__)


class RegistrationForm(FlaskForm):
    # the fields (How they look on the template, the validators to the form)
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )

    submit = SubmitField("sign up")

    # to display something to the user if error occurs
    # Called automatically when the submit happens
    # field gets the data the user is submitting
    def validate_username(self, field):
        print("validate was called🤩🤩🤩🤩", field.data)
        # check if they exist by the column name and teh data given on te for
        existing_username = User.query.filter_by(username=field.data).first()
        if existing_username:
            raise ValidationError("User name already exists")


# ---------------------------------------------------------------------------------------
# Login


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")

    def validate_username(self, field):
        existing_username = User.query.filter_by(username=field.data).first()
        if not existing_username:
            raise ValidationError("Username is incorrect")

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if user.password != field.data:
                raise ValidationError("Incorrect password")


@user_bp.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegistrationForm()
    # if post(when submit is clicked)
    if form.validate_on_submit():
        print(f"{generate_password_hash(form.password.data)}{form.password.data}")
        hashed_password = generate_password_hash(form.password.data)
        # get the user from the form
        # username = form.username.data
        # password = form.password.data
        new_user = User(
            username=form.username.data, password=hashed_password
        )  # pass the hashed password in the db
        try:
            db.session.add(new_user)
            db.session.commit()
            return "<h1>Registration successful"
        except Exception as e:
            db.session.rollback()
            return f"<h1>Error happend {str(e)}</h1>", 500
    # if GET
    return render_template("register.html", form=form)


# -------------------------------------------------------------------------------------


@user_bp.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm()
    # if post(when submit is clicked)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)  # token store in the cookie to allow the user access
        flash("You were successfully logged in")
        return redirect(url_for("movie_list_bp.movie_list_page"))
    else:
        return render_template("login.html", form=form)


# ----------------------------------------------------------------------------------------
# dashoard
@user_bp.route("/dashboard", methods=["POST"])
def welcome_page():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("welcome_page.html", username=username, password=password)


# @user_bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(somewhere)
