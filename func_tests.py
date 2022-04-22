import unittest
from flask import url_for, request
from functions import encrypt_password
from app import app
import requests
from spotify_model import load_spotify_features, generate_playlist_recommendations
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
        
    def testSpotifyGetTrackInfo(self):
        test_track_id = '3roq8qsVwzSEQA2lorvJEG'
        expected_output = ['Starting Over', 'https://open.spotify.com/track/3roq8qsVwzSEQA2lorvJEG', 'Beres Hammond', 'https://open.spotify.com/artist/2ruMkdO4e1tJWDHsYSEtxr', 'Beres Hammond Classic Songs', 'https://open.spotify.com/album/71bmlG2MmQhqYfR2ENeKwp', 'https://i.scdn.co/image/ab67616d00001e0245684482da59fdce28c8be2c']
        track_name, track_link, artist, artist_link, album,  album_link, album_pic = get_track_info(test_track_id)
        output_arr = [track_name, track_link, artist, artist_link, album,  album_link, album_pic]
        self.assertEqual(expected_output,output_arr)

    '''Test function to make sure the login page is availble and has no errors'''
    def test_index(self):
        tester  = app.test_client()
        response = tester.get('/login')
        self.assertEqual(response.status_code,200)
    
    '''Test function to make sure a user can loginm, and if it is an incorrect password show them'''
    def test_login(self):
        tester = app.test_client()
        response = tester.post('/login', data=dict(username="group5",password="group5"),
        follow_redirects  = True)
        self.assertIn(b' ', response.data)
    

    #Checks that a user can login correctly, either if it already exists will tell them or take them to the login page
    def test_user_registration(self):
        tester = app.test_client()
        response = tester.post('/signup', data=dict(username = 'random%$%', password= 'word',
        email = 'ran@gmail.com', firstname = 'Random', lastname = 'random'), follow_redirects  = True)
        self.assertIn(b'/login', response.data)  

    def test_feature_recommender(self):
        test = generate_playlist_recommendations(0,0,0)
        print(test)

    
        
    

if __name__ == "__main__":
    unittest.main()