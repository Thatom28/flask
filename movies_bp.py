from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import uuid

# from app import app

movies_bp = Blueprint("movies_bp", __name__)

db = SQLAlchemy()


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


@movies_bp.get("/")
def get_movies():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return jsonify(data)


# Task 1: Data from Azure (MSSQL)
# Clue: .all() - .get()
@movies_bp.get("/<id>")
def get_movie(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return jsonify(data)
    else:
        return jsonify({"message": "Movie not found"}), 404


# Task 4 | db.session.delete(movie)
@movies_bp.delete("/<id>")
def delete_movie(id):
    # Permission to modify the lexical scope variable
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return jsonify({"message": "Movie not found"}), 404

    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # Making the change (update/delete/create) permanent
        return jsonify({"message": "Deleted Successfully", "data": data})
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500


# Handle the error scenario
@movies_bp.post("/")
def create_movies():
    data = request.json  # body
    new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        # movies.append(new_movie)
        result = {"message": "Added successfully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500


# Task: convert to DB call
@movies_bp.put("/<id>")
def update_movie_by_id(id):
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return jsonify({"message": "Movie not found"}), 404
    body = request.json  # user

    # body - {"rating": 4}
    try:
        for key, value in body.items():
            if hasattr(filtered_movie, key):
                setattr(filtered_movie, key, value)

        db.session.commit()
        return jsonify(
            {"message": "Movie updated successfully!", "data": filtered_movie.to_dict()}
        )
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500
