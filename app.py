import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
from extensions import db

load_dotenv()  # load -> os env (enviroment variables)
print(os.environ.get("AZURE_DATABASE_URL"), os.environ.get("FORM_SECRET_KEY"))

app = Flask(__name__)

# Driver={ODBC Driver 18 for SQL Server};Server=tcp:thato.database.windows.net,1433;Database=moviesdb;Uid=thatomatlala;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# the connection string is changed if the database is changed to another platform
# connection_string = "mssql+pyodbc://thatomatlala:password1!@thato.database.windows.net:1433/moviesdb?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# Token
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")


# ----------------------------------------------------------------------------------------------


db.init_app(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)

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

if __name__ == "__main__":
    app.run(debug=True)
