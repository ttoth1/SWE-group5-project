# pylint: disable=C0114, E1101, C0103, R0903
from flask_login import UserMixin
from app import db


class Liked_Songs(db.Model):
    """Table to store track id's for a user's liked songs"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    track_id = db.Column(db.String(80))


class User_Table(db.Model, UserMixin):
    """Table to store a user's login information"""

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))


db.create_all()
