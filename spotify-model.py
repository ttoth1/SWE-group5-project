# pylint: disable=anomalous-backslash-in-string,E1101

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


pd.options.mode.chained_assignment = None


def load_spotify_features():
    # Load Spotify Song data from dataset
    spotify_data = pd.read_csv("data/model-features.csv")
    spotify_data.drop_duplicates(subset=["track_id"])
    spotify_data.dropna()
    spotify_features_df = spotify_data

    # OneHotEncode categorical features
    genre_ohe = pd.get_dummies(spotify_features_df.genre)
    key_ohe = pd.get_dummies(spotify_features_df.key)

    # Normalize numeric features
    scaled_features = MinMaxScaler().fit_transform(
        [
            spotify_features_df["acousticness"].values,
            spotify_features_df["danceability"].values,
            spotify_features_df["duration_ms"].values,
            spotify_features_df["energy"].values,
            spotify_features_df["instrumentalness"].values,
            spotify_features_df["liveness"].values,
            spotify_features_df["loudness"].values,
            spotify_features_df["speechiness"].values,
            spotify_features_df["tempo"].values,
            spotify_features_df["valence"].values,
        ]
    )

    # Replace numeric feature values with normalized values
    spotify_features_df[
        [
            "acousticness",
            "danceability",
            "duration_ms",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "speechiness",
            "tempo",
            "valence",
        ]
    ] = scaled_features.T

    # Drop columns that have little effect on predictions and columns with pre-OHE values
    spotify_features_df = spotify_features_df.drop("genre", axis=1)
    spotify_features_df = spotify_features_df.drop("artist_name", axis=1)
    spotify_features_df = spotify_features_df.drop("track_name", axis=1)
    spotify_features_df = spotify_features_df.drop("popularity", axis=1)
    spotify_features_df = spotify_features_df.drop("key", axis=1)
    spotify_features_df = spotify_features_df.drop("mode", axis=1)
    spotify_features_df = spotify_features_df.drop("time_signature", axis=1)

    # Add OneHotEncoded categorical features
    spotify_features_df = spotify_features_df.join(genre_ohe)
    spotify_features_df = spotify_features_df.join(key_ohe)
    return spotify_features_df, spotify_data


def generate_playlist_feature(feature_set: pd.DataFrame, liked_songs: pd.DataFrame):
    liked_songs_features = feature_set[
        feature_set["track_id"].isin(liked_songs["track_id"].values)
    ]
    # Find all non-playlist song features
    not_liked_songs_features = feature_set[
        ~feature_set["track_id"].isin(liked_songs["track_id"].values)
    ]
    liked_songs_features_final = liked_songs_features.drop(columns="track_id")
    return (
        liked_songs_features_final.sum(axis=0),
        not_liked_songs_features,
    )


def generate_playlist_recos(
    dataset_df: pd.DataFrame, features: pd.Series, nonplaylist_features: pd.DataFrame
):
    non_playlist_df = dataset_df[
        dataset_df["track_id"].isin(nonplaylist_features["track_id"].values)
    ]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df["sim"] = cosine_similarity(
        nonplaylist_features.drop("track_id", axis=1).values,
        features.values.reshape(1, -1),
    )[:, 0].copy()
    non_playlist_df_top = non_playlist_df.sort_values("sim", ascending=False).head(5)
    non_playlist_df_middle = non_playlist_df.sort_values("sim", ascending=False).sample(
        3
    )
    non_playlist_df_bottom = non_playlist_df.sort_values("sim", ascending=False).tail(3)
    recommendations = pd.concat(
        [non_playlist_df_top, non_playlist_df_middle, non_playlist_df_bottom]
    )
    return recommendations.sample(1)["track_id"].values[0]
