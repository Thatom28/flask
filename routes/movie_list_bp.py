from flask import Blueprint, request, render_template
from flask_sqlalchemy import SQLAlchemy
from models.movie import Movie
from extensions import db
from flask_login import login_required


movie_list_bp = Blueprint("movie_list_bp", __name__)


# Task 2: /movies-list -> Display the data on the page from Azure (MSSQL)
# Movie list dashboard
@movie_list_bp.route("/")  # HOF
@login_required
def movie_list_page():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return render_template("movie_list.html", movies=data)


# Task 3: /movies-list/99 -> Display the data on the page from Azure (MSSQL)
# Movie list detail
@movie_list_bp.route("/<id>")  # HOF
def movie_detail_page(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return render_template("movie_detail.html", movie=data)
    else:
        return "<h1>Movie not found</h1>"


@movie_list_bp.route("/add", methods=["GET"])  # HOF
def add_movie():
    return render_template("add_movie.html")


@movie_list_bp.route("/delete", methods=["POST"])  # HOF
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


@movie_list_bp.route("/success", methods=["POST"])  # HOF
def create_movie():
    # Creating a dictionary
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": request.form.get("rating"),
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer"),
    }

    new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        # movies.append(new_movie)
        return f"<h1>{data['name']} Movie added Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


@movie_list_bp.route("/update/<id>", methods=["GET"])
def update_movie(id):
    movie = Movie.query.get(id)
    if movie:
        return render_template("edit_movie.html", movie=movie)
    else:
        return "<h1>Movie not found</h1>", 404


@movie_list_bp.route("/updated/<id>", methods=["POST"])
def updated_movie_by_id(id):
    movie = Movie.query.get(id)
    if movie:
        movie.name = request.form.get("name", movie.name)
        movie.poster = request.form.get("poster", movie.poster)
        movie.rating = request.form.get("rating", movie.rating)
        movie.summary = request.form.get("summary", movie.summary)
        movie.trailer = request.form.get("trailer", movie.trailer)
        try:
            db.session.commit()
            return f"<h1>Movie updated</h1>", 500
        except Exception as e:
            return f"<h1>Error happened {str(e)}</h1>", 500
    else:
        return f"<h1>Movie not found</h1>", 500
