import unittest
from flask import url_for, request
import app
from functions import encrypt_password


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

        

if __name__ == "__main__":
    unittest.main()