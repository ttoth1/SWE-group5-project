from app import app, db
import random
import os
import base64
import flask
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
from models import Liked_Songs, User_Table
from functions import encrypt_password
from wikipedia import get_wiki_link
from tmdb import get_movie_data
from spotify_model import (
    load_spotify_features,
    generate_playlist_feature,
    generate_playlist_recommendations,
)

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




@app.route("/get_reviews")
@login_required
def foo():
    ratings = Rating.query.filter_by(username=current_user.username).all()
    return flask.jsonify(
        [
            {
                "rating": rating.rating,
                "comment": rating.comment,
                "movie_id": rating.movie_id,
            }
            for rating in ratings
        ]
    )


@app.route("/save_reviews", methods=["POST"])
def save_reviews():
    data = flask.request.json
    user_ratings = Rating.query.filter_by(username=current_user.username).all()
    new_ratings = [
        Rating(
            username=current_user.username,
            rating=r["rating"],
            comment=r["comment"],
            movie_id=r["movie_id"],
        )
        for r in data
    ]
    for rating in user_ratings:
        db.session.delete(rating)
    for rating in new_ratings:
        db.session.add(rating)
    db.session.commit()
    return flask.jsonify("Ratings successfully saved")


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
    else:
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

    else:
        flask.flash("Error: Incorrect Username or Password!")
        return flask.render_template("login.html")


MOVIE_IDS = [
    157336,  # actually IDK what this is
]


@app.route("/add_liked_song")
def add_liked_song():
    song = flask.session.get("track_id")
    new_liked_song = Liked_Songs(username=current_user.username, track_id=song)
    db.session.add(new_liked_song)
    db.session.commit()
    return flask.redirect("/index")


@app.route("/rate", methods=["POST"])
def rate():
    data = flask.request.form
    rating = data.get("rating")
    comment = data.get("comment")
    movie_id = data.get("movie_id")

    new_rating = Rating(
        username=current_user.username,
        rating=rating,
        comment=comment,
        movie_id=movie_id,
    )

    db.session.add(new_rating)
    db.session.commit()
    return flask.redirect("index")


@app.route("/")
def landing():
    if current_user.is_authenticated:
        return flask.redirect("index")
    return flask.redirect("login")


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect("login")


@app.route("/user_profile", methods=["POST"])
def user_profle():
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    return flask.render_template(
        "user_profile.html", firstname=firstname, lastname=lastname, email=email
    )


# spotify_features_df, spotify_data = load_spotify_features()
@app.route("/index")
@login_required
def index():
    movie_id = random.choice(MOVIE_IDS)

    liked_song_list = []
    liked_song_query = Liked_Songs.query.filter_by(username=current_user.username).all()
    for track_id in liked_song_query:
        liked_song_list.append(track_id)
    liked_songs_vector, not_liked_songs_features = generate_playlist_feature(
        spotify_features_df, liked_song_list
    )
    flask.session["track_id"] = generate_playlist_recommendations(
        spotify_data, liked_songs_vector, not_liked_songs_features
    )

    # API calls
    (title, tagline, genre, poster_image) = get_movie_data(movie_id)
    wikipedia_url = get_wiki_link(title)

    # ratings = Rating.query.filter_by(movie_id=movie_id).all()

    return flask.render_template(
        "main.html",
        title=title,
        tagline=tagline,
        genre=genre,
        poster_image=poster_image,
        wiki_url=wikipedia_url,
        # ratings=ratings,
        movie_id=movie_id,
        track_id=flask.session.get("track_id"),
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
