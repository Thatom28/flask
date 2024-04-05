import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
from extensions import db
from flask_login import LoginManager
from models.users import User


# server = 'localhost'
# database = 'moviesdb'
# username = 'MD/E1005292'
# driver_name = "ODBC Driver 17 for SQL Server"
# connection_string = f"mssql+pyodbc://{username}:@{server}/{database}?driver={driver_name}"

load_dotenv()  # load -> os env (enviroment variables)
print(os.environ.get("AZURE_DATABASE_URL"), os.environ.get("FORM_SECRET_KEY"))

app = Flask(__name__)
# for azure connection
# connection_string = os.environ.get("AZURE_DATABASE_URL")
connection_string = os.environ.get("LOCAL_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# Token
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)


# ----------------------------------------------------------------------------------------------


db.init_app(app)


# -----------------------------------------------------------------------------


@app.route("/movie/add")
def add_movie():
    return render_template("add_movie.html")


# ----------------------------------------------------------------------------

from routes.about_bp import about_bp

app.register_blueprint(about_bp, url_prefix="/about")


# ------------------------------------------------------------------------------------------------

from routes.movies_bp import movies_bp

app.register_blueprint(movies_bp, url_prefix="/movies")


# --------------------------------------------------------------------------
from routes.movie_list_bp import movie_list_bp

app.register_blueprint(movie_list_bp, url_prefix="/movie_list")

# ----------------------------------------------------------
from routes.user_bp import user_bp

app.register_blueprint(user_bp)
# --------------------------------------------------------------------------
# main
from routes.main_bp import main_bp

app.register_blueprint(main_bp)


# verifys the user with this
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.drop_all()  # delete the tables in the database
        # db.create_all()  # Sync tables to db
        print("creation done")
except Exception as e:
    print("Error connecting to the database:", e)

if __name__ == "__main__":
    app.run(debug=True)
