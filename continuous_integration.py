import unittest
from flask import url_for, request
from functions import encrypt_password
from app import app
from spotify_model import load_spotify_features

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