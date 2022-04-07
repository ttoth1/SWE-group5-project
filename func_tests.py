import unittest
from flask import url_for, request
import app

test_client = app.app.test_client()

with test_client:
    response = test_client.get(url_for('user_profile') )
    assert request.path == url_for('userprofile.html')
    pass
