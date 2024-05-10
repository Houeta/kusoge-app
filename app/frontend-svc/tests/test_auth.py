import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, Request

from auth import login, signup  # Importing functions from auth.py

class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
    
    @patch('auth.requests.post')
    def test_login_missing_credentials(self, mock_requests_post):
        mock_requests_post.return_value.text = "missing credentials"
        mock_requests_post.return_value.status_code = 401
        with self.app.test_request_context('/', method='POST', data={'email': '', 'password': ''}):
            request = Request.from_values(method='POST', data={'email': '', 'password': ''})
            response_text, status_code = login(request)
            self.assertEqual(response_text, "missing credentials")
            self.assertEqual(status_code, 401)
    
    @patch('auth.requests.post')
    def test_login_success(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.text = "1:John Doe"
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response
        with self.app.test_request_context('/', method='POST', data={'email': 'john@example.com', 'password': 'password'}):
            request = Request.from_values(method='POST', data={'email': 'john@example.com', 'password': 'password'})
            response_text, status_code = login(request)
            self.assertEqual(response_text, "1:John Doe")
            self.assertEqual(status_code, 200)
    
    @patch('auth.requests.post')
    def test_signup_missing_credentials(self, mock_requests_post):
        mock_requests_post.return_value.text = "missing credentials"
        mock_requests_post.return_value.status_code = 401
        with self.app.test_request_context('/', method='POST', data={'email': '', 'password': ''}):
            request = Request.from_values(method='POST', data={'email': '', 'password': ''})
            response_text, status_code = signup(request)
            self.assertEqual(response_text, "missing credentials")
            self.assertEqual(status_code, 401)
    
    @patch('auth.requests.post')
    def test_signup_success(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_requests_post.return_value.text = ""
        mock_requests_post.return_value.status_code = 201
        with self.app.test_request_context('/', method='POST', data={'email': 'john@example.com', 'name': 'John Doe', 'password': 'password'}):
            request = Request.from_values(method='POST', data={'email': 'john@example.com', 'name': 'John Doe', 'password': 'password'})
            response_text, status_code = signup(request)
            self.assertEqual(response_text, "")
            self.assertEqual(status_code, 201)

if __name__ == '__main__':
    unittest.main()
