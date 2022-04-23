# pylint: disable=E1101, W1508, C0116

"""This file runs all flask routes."""

import os
import base64
import flask
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
from models import Liked_Songs, Skipped_Songs, User_Table
from app import app, db
from functions import encrypt_password
from spotify_model import (
    load_spotify_features,
    generate_playlist_feature,
    generate_playlist_recommendations,
)
from get_track_info import get_track_info

spotify_features_df, spotify_data = load_spotify_features()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


@bp.route("/spotify_login")
def spotify_login():
    return flask.render_template("index.html")


app.register_blueprint(bp)


@login_manager.user_loader
def load_user(user_name):
    return User_Table.query.get(user_name)


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    print(flask.request.form.get)
    username = flask.request.form.get("username")
    email = flask.request.form.get("email")
    firstname = flask.request.form.get("firstname")
    lastname = flask.request.form.get("lastname")
    raw_password = flask.request.form.get("password")
    password = encrypt_password(raw_password=raw_password)
    user = User_Table.query.filter_by(username=username).first()
    if user:
        flask.flash("Error: username already exists!")
        return flask.render_template("signup.html")
    user = User_Table(
        username=username,
        password=password,
        firstname=firstname,
        lastname=lastname,
        email=email,
    )
    db.session.add(user)
    db.session.commit()
    return flask.redirect(flask.url_for("login"))


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    raw_password = flask.request.form.get("password")
    password = encrypt_password(raw_password=raw_password)
    user = User_Table.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))
    flask.flash("Error: Incorrect Username or Password!")
    return flask.render_template("login.html")


@app.route("/about_us")
def about_us():
    return flask.render_template("about_us.html")


@app.route("/add_liked_song")
def add_liked_song():
    song = flask.session.get("track_id")
    new_liked_song = Liked_Songs(username=current_user.username, track_id=song)
    db.session.add(new_liked_song)
    db.session.commit()
    return flask.redirect("/index")


@app.route("/add_skipped_song")
def add_skipped_song():
    song = flask.session.get("track_id")
    new_skipped_song = Skipped_Songs(username=current_user.username, track_id=song)
    db.session.add(new_skipped_song)
    db.session.commit()
    return flask.redirect("/index")


@app.route("/remove_liked_song", methods=["POST"])
def remove_liked_song():
    username = current_user.username
    track_id = flask.request.form.get("Remove")
    Liked_Songs.query.filter_by(username=username, track_id=track_id).delete()
    db.session.commit()
    return flask.redirect("user_profile")


@app.route("/get_liked_songs", methods=["POST"])
def get_liked_songs():
    username = current_user.username
    liked_songs = []
    liked_song_query = db.session.query(Liked_Songs.track_id).filter_by(
        username=username
    )
    if liked_song_query:
        for song_id in liked_song_query:
            track_info = get_track_info(str(song_id[0]))
            (
                track_name,
                track_link,
                artist,
                artist_link,
                album,
                album_link,
                album_pic,
            ) = track_info
            temp = [
                track_name,
                track_link,
                artist,
                artist_link,
                album,
                album_link,
                album_pic,
                str(song_id[0]),
            ]
            liked_songs.append(temp)

    return liked_songs


@app.route("/")
def landing():
    if current_user.is_authenticated:
        return flask.redirect("index")
    return flask.render_template("landing.html")


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for("landing"))


@app.route("/user_profile", methods=["GET", "POST"])
def user_profle():
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    liked_songs = get_liked_songs()
    return flask.render_template(
        "user_profile.html",
        firstname=firstname,
        lastname=lastname,
        email=email,
        liked_songs=liked_songs,
        num_songs=len(liked_songs),
    )


@app.route("/index")
@login_required
def index():
    liked_song_list = []
    skipped_song_list = []

    liked_song_query = Liked_Songs.query.filter_by(username=current_user.username).all()
    for track in liked_song_query:
        liked_song_list.append(track.track_id)

    skipped_song_query = Skipped_Songs.query.filter_by(
        username=current_user.username
    ).all()

    for track in skipped_song_query:
        skipped_song_list.append(track.track_id)

    liked_songs_vector, not_liked_songs_features = generate_playlist_feature(
        spotify_features_df, liked_song_list, skipped_song_list
    )
    if not liked_song_list and not skipped_song_list:
        flask.session["track_id"] = "7GhIk7Il098yCjg4BQjzvb"
    else:
        flask.session["track_id"] = generate_playlist_recommendations(
            spotify_data, liked_songs_vector, not_liked_songs_features
        )
    current_track = flask.session.get("track_id")
    track_info = get_track_info(current_track)
    (
        track_name,
        track_link,
        artist,
        artist_link,
        album,
        album_link,
        album_pic,
    ) = track_info

    return flask.render_template(
        "main.html",
        track_id=flask.session.get("track_id"),
        track_name=track_name,
        track_link=track_link,
        artist=artist,
        artist_link=artist_link,
        album=album,
        album_link=album_link,
        album_pic=album_pic,
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
