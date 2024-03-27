from flask import Blueprint, request, render_template
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid

user_bp = Blueprint("user_bp", __name__)

db = SQLAlchemy()


class User(db.Model):
    # the table name to point to
    __tablename__ = "users"
    # add its columns                  #it will create random string for id| no need to add
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    usename = db.Column(db.String(50))
    password = db.Column(db.String(50))

    # how the data should loook like in JSON (the keys)
    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
