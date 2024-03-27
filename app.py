import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid

load_dotenv()  # load -> os env (enviroment variables)
print(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__)

# Driver={ODBC Driver 18 for SQL Server};Server=tcp:thato.database.windows.net,1433;Database=moviesdb;Uid=thatomatlala;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# the connection string is changed if the database is changed to another platform
# connection_string = "mssql+pyodbc://thatomatlala:password1!@thato.database.windows.net:1433/moviesdb?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


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


@app.get("/movies")
def get_movie():
    movie_list = Movie.query.all()
    data = [
        movie.to_dict() for movie in movie_list
    ]  # converting a list of dictionaries
    return jsonify(data)


# ----------------------------------------------------------------------------------
# task 1 get movie by id
@app.get("/movies/<id>")
def get_movie_by_id(id):
    movie = Movie.query.get(id)
    if movie:
        data = [movie.to_dict()]  # converting a list of dictionaries
        return jsonify(data)
    else:
        result = {"message": "movies not found"}


# ------------------------------------------------------------------------------------------------
# Task 3: display a movie by id
@app.route("/movies_list/<id>")
def movie_id_page(id):
    movie = Movie.query.get(id)
    if movie:
        data = [movie.to_dict()]  # converting a list of dictionaries
        return render_template("movie_list.html", movies=data)
    else:
        "<h1>Movie not found</h1>"


# --------------------------------------------------------------------------------------------------------------------------------
# task 4
@app.delete("/movies/<id>")  # <> converts to a variable
def delete_movie(id):
    movie = Movie.query.get(id)
    try:
        data = movie.to_dict()
        db.session.delete(movie)
        # commit for (create|delete|update)
        db.session.commit()  # deleted permanently, cannot rollback
        return jsonify({"message": "movie not found", "data": data})
    except Exception as e:
        db.session.rollback()  # undo the change
        return jsonify({"message": "movie not found"})


# Task 4 | db.session.delete(movie)
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     # Permission to modify the lexical scope variable
#     filtered_movie = Movie.query.get(id)
#     if not filtered_movie:
#         return jsonify({"message": "Movie not found"}), 404

#     try:
#         data = filtered_movie.to_dict()
#         db.session.delete(filtered_movie)
#         db.session.commit()  # Making the change (update/delete/create) permanent
#         return jsonify({"message": "Deleted Successfully", "data": data})
#     except Exception as e:
#         db.session.rollback()  # Undo the change
#         return jsonify({"message": str(e)}), 500

# --------------------------------------------------------------------------------------------------------------------
# Task 5: delete on the wweb page
# @app.route("/movies/delete/<id>")  # <> converts to a variable
# def delete_movie(id):
#     movie = Movie.query.get(id)
#     try:
#         data = movie.to_dict()
#         db.session.delete(movie)
#         # commit for (create|delete|update)
#         db.session.commit()  # deleted permanently, cannot rollback
#         return render_template("movie_list")
#     except Exception as e:
#         db.session.rollback()  # undo the change
#         return jsonify({"message": "movie not found"})


# -------------------------------------------------------------------------------------------------------------------
# Adding to the database
# randomly generate pk
@app.post("/movies")
def create_movie():
    data = request.json
    new_movie = Movie(
        name=data["name"],
        poster=data["poster"],
        rating=data["rating"],
        summary=data["summary"],
        trailer=data["trailer"],
    )
    # if the names are the same as the ones given in the other side
    # new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        result = {"message": "movies added succsefully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "movie not added"})


# --------------------------------------------------------------------------------------------
@app.put("/movies/update/<id>")
def update_movie_by_id(id):
    movie = Movie.query.get(id)
    if movie:
        data = request.json
        movie.name = data.get("name", movie.name)
        movie.poster = data.get("poster", movie.poster)
        movie.rating = data.get("rating", movie.rating)
        movie.summary = data.get("summary", movie.summary)
        movie.trailer = data.get("trailer", movie.trailer)
        db.session.commit()
        return jsonify({"message": "Updated Successfully", "data": movie.to_dict()})
    else:
        return jsonify({"message": "Movie not found"}), 404


# the home page what should we return
# this is a page
@app.route("/")
def hello_world():
    return "<h1>Hello, Sanlam🌍!</h1>"


users = [
    {
        "name": "Thato",
        "pic": "https://i.pinimg.com/736x/30/b6/fc/30b6fcaec93c8d7d21dfb930d661269b.jpg",
        "pro": True,
    },
    {
        "name": "Mpumi",
        "pic": "https://i.pinimg.com/736x/30/b6/fc/30b6fcaec93c8d7d21dfb930d661269b.jpg",
        "pro": False,
    },
    {
        "name": "Lethabo",
        "pic": "https://i.pinimg.com/736x/30/b6/fc/30b6fcaec93c8d7d21dfb930d661269b.jpg",
        "pro": True,
    },
]
name = "Thato"
hobbies = ["gaming", "codong", "gym", "reading"]


# About page
@app.route("/about")
def about():
    return render_template("about.html", users=users)


@app.route("/profile")
def profile():
    return render_template("profile.html", name=name, hobbies=hobbies)


# ---------------------------------------------------------------------------
#                                DAY 22

# @app.route("/movie_list")
# def movie_list():
#     return render_template("movie_list.html", movies=movies)


# @app.route("/movie_list/<id>")
# def detail(id):
#     movie = next((movie for movie in movies if movie["id"] == id), None)
#     if movie:
#         return render_template("movie_detail.html", id=id, movie=movie)
#     else:
#         return "<h1>movie not found</h1>"


# forms template
@app.route("/forms")
def forms():
    return render_template("forms.html", users=users)


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html")


# ----------------------------------------------------------------------------
# when the bustton is clicked
# @app.route("/dashboard", methods=["POST"])
# def dashboard_page():
#     # to get th eusername form the form
#     username = request.form.get("username")
#     password = request.form.get("password")
#     print("dashboard page", username, password)
#     # instead of a page it will display a header
#     return "<h1>Hi {{username}} </h1>"


# welcome message
@app.route("/dashboard", methods=["POST"])
def welcome_page():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("welcome_page.html", username=username, password=password)


# --------------------------------------------------------------------


@app.route("/movie/add")
def add_movie():
    return render_template("add_movie.html")


# Task - /movies/add -> Add movie form (5 fields) -> Submit -> /movies-list
# @app.route("/movie/add", methods=["POST"])
# def movie_added():
#     movie_name = request.form.get("movie_name")
#     movie_poster = request.form.get("movie_poster")
#     movie_rating = request.form.get("movie_rating")
#     movie_summary = request.form.get("movie_summary")
#     movie_trailer = request.form.get("movie_trailer")
#     new_movie = {
#         "name": movie_name,
#         "poster": movie_poster,
#         "summary": movie_summary,
#         "rating": movie_rating,
#         "trailer": movie_trailer,
#     }
#     ids = [int(movie["id"]) for movie in movies]
#     largest_id = max(ids)
#     new_movie["id"] = str(largest_id + 1)
#     movies.append(new_movie)
#     return render_template("movie_list.html", movies=movies)


# --------------------------------------------------------------------------------------------------------------------------------
# Task 2: display all to the screen
@app.route("/movie-list")
def movie_list_page():
    movie_list = Movie.query.all()
    data = [movie.to_dict() for movie in movie_list]
    return render_template("movie_list.html", movies=data)


# --------------------------------------------------------------------------
# deleting a movie
@app.route("/movie-list/delete", methods=["POST"])  # HOF
def delete_movie_by_id():
    print(request.form.get("movie_id"))
    id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return "<h1>Movie not found</h1>", 404

    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # Making the change (update/delete/create) permanent
        return f"<h1>{data['name']} Movie deleted Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


# ---------------------------------------------------------------------------


@app.route("/movie-list/add", methods=["POST"])  # HOF
def add_movie_to_list():
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": request.form.get("rating"),
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer"),
    }
    try:
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        return f"<h1>{new_movie.name} Movie added Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


# ----------------------------------------------------------------------------


@app.route("/movie/update/<id>")
def edit_movie_by_id(id):
    movie = Movie.query.get(id)
    if movie:
        movie_name = request.form.get("movie_name", movie.name)
        movie_poster = request.form.get("movie_poster", movie.poster)
        movie_rating = request.form.get("movie_rating", movie.rating)
        movie_summary = request.form.get("movie_summary", movie.summary)
        movie_trailer = request.form.get("movie_trailer", movie.trailer)
    movie = Movie(
        name=movie_name,
        poster=movie_poster,
        rating=movie_rating,
        summary=movie_summary,
        trailer=movie_trailer,
    )
    try:
        db.session.commit()
        return jsonify({"message": "Updated Successfully", "data": movie.to_dict()})
    except Exception as e:
        return jsonify({"message": "Movie not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
