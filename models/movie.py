import uuid

# can import using relaive import | . current folder |..one folder back(up) (relative import)
# reads from the current folder
# from ..extensions import db

# Absolute reads from the base
# flask/models/movie
from extensions import db


class Movie(db.Model):
    # the table name to point to
    __tablename__ = "movies"

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
