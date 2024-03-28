import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
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
    username = db.Column(db.String(50))
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


# --------------------------------------------------------------------------
from user_bp import user_bp

app.register_blueprint(user_bp, url_prefix="/user")

# -------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class RegistrationForm(FlaskForm):
    # the fields (How they look on the template, the validators to the form)
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )

    submit = SubmitField("sign up")


@app.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegistrationForm()
    # (on "POST" if the submit button is clicked)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return "<h1>Registration successful"
        except Exception as e:
            db.session.rollback()
            return f"<h1>Error happend {str(e)}</h1>", 500
    # for GET
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
