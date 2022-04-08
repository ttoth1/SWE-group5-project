from pickle import TRUE
import unittest
from flask import url_for, request
<<<<<<< HEAD
from app import app
=======
import models
import routes
>>>>>>> a9d026278669fd8fccef0caa57f1586da617eea5
from functions import encrypt_password
from app import app
import requests
from models import User_Table, Liked_Songs

class testPasswordEncryption(unittest.TestCase):
    
    
    def test_password_password(self):
        test_password = 'password'
        expected_output = 'cGFzc3dvcmQ='
        actual_output = encrypt_password(test_password)
        self.assertEqual(expected_output,actual_output)
        pass
    
    

    def test_index(self):
        tester  = app.test_client()
        response = tester.get('/login')
        print(response)
        self.assertEqual(response.status_code,200)
    

    def test_login(self):
        tester = app.test_client()
        response = tester.post('/login', data=dict(username="group5",password="group5"),
        follow_redirects  = True)
        self.assertIn(b'See', response.data)
    

    #Checks that a user can login correctly, either if it already exists will tell them or take them to the login page
    def test_user_registration(self):
        tester = app.test_client()
        response = tester.post('/signup', data=dict(username = 'random%$%', password= 'word',
        email = 'ran@gmail.com', firstname = 'Random', lastname = 'random'), follow_redirects  = True)
        self.assertIn(b'/login', response.data)  

if __name__ == "__main__":
    unittest.main()