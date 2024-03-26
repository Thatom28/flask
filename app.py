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


# --------------------------------------------------------------------------------------------------------------------------------
# Task 2: display all to the screen
@app.route("/movies_list")
def movie_list_page():
    movie_list = Movie.query.all()
    data = [movie.to_dict() for movie in movie_list]
    return render_template("movie_list.html", movies=data)


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
@app.put("/movies/<id>")
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


# local data
# movies = [
#     {
#         "id": "99",
#         "name": "Vikram",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
#         "rating": 8.4,
#         "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
#         "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
#     },
#     {
#         "id": "100",
#         "name": "RRR",
#         "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
#         "rating": 8.8,
#         "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
#         "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
#     },
#     {
#         "id": "101",
#         "name": "Iron man 2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
#         "rating": 7,
#         "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
#         "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
#     },
#     {
#         "id": "102",
#         "name": "No Country for Old Men",
#         "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
#         "rating": 8.1,
#         "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
#         "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
#     },
#     {
#         "id": "103",
#         "name": "Jai Bhim",
#         "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
#         "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
#         "rating": 8.8,
#         "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
#     },
#     {
#         "id": "104",
#         "name": "The Avengers",
#         "rating": 8,
#         "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
#         "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
#         "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
#     },
#     {
#         "id": "105",
#         "name": "Interstellar",
#         "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
#         "rating": 8.6,
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
#         "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
#     },
#     {
#         "id": "106",
#         "name": "Baahubali",
#         "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
#         "rating": 8,
#         "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
#         "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
#     },
#     {
#         "id": "107",
#         "name": "Ratatouille",
#         "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
#         "rating": 8,
#         "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
#         "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
#     },
#     {
#         "name": "PS2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
#         "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
#         "rating": 8,
#         "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
#         "id": "108",
#     },
#     {
#         "name": "Thor: Ragnarok",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
#         "rating": 8.8,
#         "trailer": "https://youtu.be/NgsQ8mVkN8w",
#         "id": "109",
#     },
# ]


# jinja2 - templates  how we maipulate html in python
# /movies -> Json
# get part of it
# @app.get("/movies")
# def get_movies():
#     # library from flask
#     return jsonify(movies)


# Ceate a new movie


# @app.post("/movies")
# def create_movie():
#     new_movie = request.json  # get data from json
#     movies.append(new_movie)
#     result = {"message": "movies added succsefully"}
#     return jsonify(result)

# -------------------------------------------------------------------------------------------
# create an id that is one more than the last and send lastest data


# @app.post("/movies")
# def create_movie():
#     largest_id = 0
#     for movie in movies:
#         movie_id = int(movie["id"])
#         if movie_id > largest_id:
#             largest_id = movie_id
#     new_movie = request.json  # get data from json
#     new_movie["id"] = str(movie_id + 1)  # add one to the max Id
#     movies.append(new_movie)
#     result = {"message": "movies added succsefully"}
#     return jsonify(result)
# ---------------------------------------------------------------------------------------------
# Above simplified

# @app.post("/movies")
# def create_movie():
#     new_movie = request.json  # get data from json
#     ids = [int(movie["id"]) for movie in movies]
#     largest_id = max(ids)
#     new_movie["id"] = str(largest_id + 1)  # add one to the max Id
#     movies.append(new_movie)
#     result = {"message": "movies added succsefully"}
#     return jsonify(result), 201


# -------------------------------------------------------------------------------------------------
# get movie by id
# @app.get("/movies/<id>")  # <> converts to a variable
# def get_movie_by_id(id):
#     movie = [movie for movie in movies if movie["id"] == id]
#     return movie[0]


# -----------------------------------------------------------------------------------------------
# Get movie by id error handling
# @app.get("/movies/<id>")  # <> converts to a variable
# def get_movie_by_id(id):
#     movie = [movie for movie in movies if movie["id"] == id]
#     if movie: #if movie was found
#         return movie[0]
#     else:
#         result = {"message": "movies not found"}
#         return jsonify(result), 404

# ------------------------------------------------------------------------------------------------
# Generator expression using the above code
# @app.get("/movies/<id>")  # <> converts to a variable
# def get_movie_by_id(id):
#     #() -> generator expression therefore no need for movies[0]
#     # loop stops as soon as the match is found
#     # better perfomance
#     movie = next((movie for movie in movies if movie["id"] == id), None)  # (expression, default value)
#     if movie:
#         return movie
#     else:
#         result = {"message": "movies not found"}
#         return jsonify(result), 404


# ---------------------------------------------------------------------------------------------
# Task - 1.1 - Negative scenario | Generator expression
# message - movie not found | status_code - 404
# @app.get("/movies/<id>")  # <> converts to a variable
# def get_movie_by_id(id):
#     movie = next(
#         (movie for movie in movies if movie["id"] == id), None
#     )  # (expression, default value)
#     if movie:
#         return movie
#     else:
#         result = {"message": "movies not found"}
#         return jsonify(result), 404


# --------------------------------------------------------------------------------------------------------------------------------
# Task - 2
# Create Delete API for movies
# @app.delete("/movies/<id>")  # <> converts to a variable
# def delete_movie(id):
##            generator expression                           default value
#     movie = next((movie for movie in movies if movie["id"] == id), None)
#     message = {"message": "Movie deleted sucessfully"}
#     movies.remove(movie)
#     return jsonify(movie, message)


# # ---------------------------------------------------------------------------------------------
#  Task - 2.1 Negative scenario
# Create Delete API for movies


# @app.delete("/movies/<id>")  # <> converts to a variable
# def delete_movie(id):
#     movie = next((movie for movie in movies if movie["id"] == id), None)
#     if movie:
#         message = "Movie deleted sucessfully"
#         movies.remove(movie)
#         return jsonify({"data": movie, "message": "Movie updated sucessfully"})
#     else:
#         result = {"message": "movies not found"}
#         return jsonify(result), 404


# --------------------------------------------------------------------------------------------------
# updating the movie
# @app.put("/movies/<id>")  # <> converts to a variable
# def update_movie(id):
#     updates = request.json  # get the data from json
#     movie = next(
#         (movie for movie in movies if movie["id"] == id), None
#     )  # find the movie id
#     if movie:
#         movie.update(updates)
#         return jsonify({"data": movie, "message": "Movie updated sucessfully"})
#     else:
#         result = {"message": "movies not found"}
#         return jsonify(result), 404


# ---------------------------------------------------------------------------------------
# using the index and enumerate

# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     movie_idx = next((idx for idx, movie in enumerate(movies) if movie["id"] == id), None) # same memory
#     body = request.json
#     movies[movie_idx] = {**movies[movie_idx], **body}


# data = [movie[key] = value for key,value in updates.items()]
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


@app.route("/add")
def add_movie():
    return render_template("add_movie.html")


# Task - /movies/add -> Add movie form (5 fields) -> Submit -> /movies-list
@app.route("/movie/add", methods=["POST"])
def movie_added():
    movie_name = request.form.get("movie_name")
    movie_poster = request.form.get("movie_poster")
    movie_rating = request.form.get("movie_rating")
    movie_summary = request.form.get("movie_summary")
    movie_trailer = request.form.get("movie_trailer")
    new_movie = {
        "name": movie_name,
        "poster": movie_poster,
        "summary": movie_summary,
        "rating": movie_rating,
        "trailer": movie_trailer,
    }
    ids = [int(movie["id"]) for movie in movies]
    largest_id = max(ids)
    new_movie["id"] = str(largest_id + 1)
    movies.append(new_movie)
    return render_template("movie_list.html", movies=movies)


# deleting a movie
if __name__ == "__main__":
    app.run(debug=True)

# -----------------------MY BIT--------------------------------------------------
# items = []


# @app.route("/")
# def index():
#     item_list = [{"index": i, "item": item} for i, item in enumerate(items)]
#     return render_template("index.html", items=item_list)


# @app.route("/add_item", methods=["POST"])
# def add_item():
#     name = request.form["name"]
#     description = request.form["description"]
#     if name and description:
#         items.append({"name": name, "description": description})
#     return redirect(url_for("index"))


# @app.route("/remove/<id>", methods=["DELETE"])
# def remove_item(id):
#     item = [item for item in items if item["id"] == id]
#     items.remove(item[0])
#     return redirect(url_for("index"))


# if __name__ == "__main__":
# app.run(debug=True)
# -------------------------------------MY BIT END--------------------------------------------------
