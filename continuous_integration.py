import unittest
from flask import url_for, request
from functions import encrypt_password
from spotify_model import load_spotify_features
from get_track_info import get_track_info

class testPasswordEncryption(unittest.TestCase):
    
    
    def test_password_password(self):
        test_password = 'password'
        expected_output = 'cGFzc3dvcmQ='
        actual_output = encrypt_password(test_password)
        self.assertEqual(expected_output,actual_output)
        pass
    
    
    def testSpotifyLoadFeatures(self):
        (spotify_features_df, spotify_data) = load_spotify_features()
        actual_output = (str(type(spotify_data)), str(type(spotify_features_df)))
        expected_output = ('<class \'pandas.core.frame.DataFrame\'>',
        '<class \'pandas.core.frame.DataFrame\'>')
        self.assertEqual(expected_output,actual_output)
    

    ## Server Client Test for Spotify APU
    def testSpotifyGetTrackInfo(self):
        test_track_id = '3roq8qsVwzSEQA2lorvJEG'
        expected_output = ['Starting Over', 'https://open.spotify.com/track/3roq8qsVwzSEQA2lorvJEG', 'Beres Hammond', 'https://open.spotify.com/artist/2ruMkdO4e1tJWDHsYSEtxr', 'Beres Hammond Classic Songs', 'https://open.spotify.com/album/71bmlG2MmQhqYfR2ENeKwp', 'https://i.scdn.co/image/ab67616d00001e0245684482da59fdce28c8be2c']
        track_name, track_link, artist, artist_link, album,  album_link, album_pic = get_track_info(test_track_id)
        output_arr = [track_name, track_link, artist, artist_link, album,  album_link, album_pic]
        self.assertEqual(expected_output,output_arr)
