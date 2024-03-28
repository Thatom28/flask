import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
from about_bp import about_bp
import uuid


load_dotenv()  # load -> os env (enviroment variables)
print(os.environ.get("AZURE_DATABASE_URL"), os.environ.get("FORM_SECRET_KEY"))

app = Flask(__name__)

# Driver={ODBC Driver 18 for SQL Server};Server=tcp:thato.database.windows.net,1433;Database=moviesdb;Uid=thatomatlala;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# the connection string is changed if the database is changed to another platform
# connection_string = "mssql+pyodbc://thatomatlala:password1!@thato.database.windows.net:1433/moviesdb?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy()
# Token
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")


# model (SQLAlchemy)  == schema
# inheriting from db.model
class Movie(db.Model):
    # the table name to point to
    __tablename__ = "movies"
    # add its columns                  #it will create random string for id| no need to add
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))

    # how the data should loook like in JSON (the keys)

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }


# ----------------------------------------------------------------------------------------------
# Home work

# class User(db.Model):
#     # the table name to point to
#     __tablename__ = "users"
#     # add its columns                  #it will create random string for id| no need to add
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     username = db.Column(db.String(50))
#     password = db.Column(db.String(50))


#     # how the data should loook like in JSON (the keys)
#     def user_to_dict(self):
#         # the name the front end wants the key to be
#         return {
#             "id": self.id,
#             "username": self.username,
#             "password": self.password,
#         }
# --------------------------------------------------------------------------------------------
class User(db.Model):
    # the table name to point to
    __tablename__ = "users"
    # add its columns                  #it will create random string for id| no need to add
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))

    # how the data should loook like in JSON (the keys)
    def user_to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


db.init_app(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)
# -------------------------------------------------------------------------------------------
# create a table if its not in the database
# db.create_all()


# --------------------------------------------------------------------------------------------
# the home page what should we return
# this is a page
@app.route("/")
def hello_world():
    return "<h1>Hello, Sanlam🌍!</h1>"


name = "Thato"
hobbies = ["gaming", "codong", "gym", "reading"]


@app.route("/profile")
def profile():
    return render_template("profile.html", name=name, hobbies=hobbies)


# welcome message
@app.route("/dashboard", methods=["POST"])
def welcome_page():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("welcome_page.html", username=username, password=password)


# -----------------------------------------------------------------------------


@app.route("/movie/add")
def add_movie():
    return render_template("add_movie.html")


# ----------------------------------------------------------------------------


app.register_blueprint(about_bp, url_prefix="/about")


# ------------------------------------------------------------------------------------------------

from movies_bp import movies_bp

app.register_blueprint(movies_bp, url_prefix="/movies")


# --------------------------------------------------------------------------
from movie_list_bp import movie_list_bp

app.register_blueprint(movie_list_bp, url_prefix="/movie_list")

# -------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


# --------------------------------------------------------------------------------------------------------------------------------
# Register
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


# --------------------------------------------------------------------------
from user_bp import user_bp

app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.run(debug=True)
