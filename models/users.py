from extensions import db
import uuid
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # the table name to point to
    __tablename__ = "users"
    # add its columns                  #it will create random string for id| no need to add
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200))

    # how the data should loook like in JSON (the keys)
    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
