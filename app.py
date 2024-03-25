from flask import Flask, jsonify, request, render_template, url_for, redirect

app = Flask(__name__)


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


@app.route("/movie_list")
def movie_list():
    return render_template("movie_list.html", movies=movies)


@app.route("/movie_list/<id>")
def detail(id):
    movie = next((movie for movie in movies if movie["id"] == id), None)
    if movie:
        return render_template("movie_detail.html", id=id, movie=movie)
    else:
        return "<h1>movie not found</h1>"


# local data
movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]


# jinja2 - templates  how we maipulate html in python
# /movies -> Json
# get part of it
@app.get("/movies")
def get_movies():
    # library from flask
    return jsonify(movies)


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
@app.post("/movies")
def create_movie():
    new_movie = request.json  # get data from json
    ids = [int(movie["id"]) for movie in movies]
    largest_id = max(ids)
    new_movie["id"] = str(largest_id + 1)  # add one to the max Id
    movies.append(new_movie)
    result = {"message": "movies added succsefully"}
    return jsonify(result), 201


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
@app.get("/movies/<id>")  # <> converts to a variable
def get_movie_by_id(id):
    movie = next(
        (movie for movie in movies if movie["id"] == id), None
    )  # (expression, default value)
    if movie:
        return movie
    else:
        result = {"message": "movies not found"}
        return jsonify(result), 404


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


@app.delete("/movies/<id>")  # <> converts to a variable
def delete_movie(id):
    movie = next((movie for movie in movies if movie["id"] == id), None)
    if movie:
        message = "Movie deleted sucessfully"
        movies.remove(movie)
        return jsonify({"data": movie, "message": "Movie updated sucessfully"})
    else:
        result = {"message": "movies not found"}
        return jsonify(result), 404


# --------------------------------------------------------------------------------------------------
# updating the movie
@app.put("/movies/<id>")  # <> converts to a variable
def update_movie(id):
    updates = request.json  # get the data from json
    movie = next(
        (movie for movie in movies if movie["id"] == id), None
    )  # find the movie id
    if movie:
        movie.update(updates)
        return jsonify({"data": movie, "message": "Movie updated sucessfully"})
    else:
        result = {"message": "movies not found"}
        return jsonify(result), 404


# ---------------------------------------------------------------------------------------
# using the index and enumerate

# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     movie_idx = next((idx for idx, movie in enumerate(movies) if movie["id"] == id), None) # same memory
#     body = request.json
#     movies[movie_idx] = {**movies[movie_idx], **body}


# data = [movie[key] = value for key,value in updates.items()]
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
