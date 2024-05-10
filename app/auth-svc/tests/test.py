import unittest
from unittest.mock import patch, MagicMock
import psycopg2
from app import app, _get_db_connection

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'OK!')

    @patch('psycopg2.connect')
    def test_get_db_connection(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_connect.return_value = mock_connection
        conn = _get_db_connection()
        self.assertEqual(conn, mock_connection)

    def test_login_missing_fields(self):
        response = self.app.post('/login')
        self.assertEqual(response.status_code, 401)

    @patch('psycopg2.connect')
    def test_login_invalid_email(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_cursor = MagicMock(name='cursor_mock')
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_connection

        response = self.app.post('/login', data={'email': 'invalid@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 404)

    @patch('psycopg2.connect')
    def test_login_invalid_password(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_cursor = MagicMock(name='cursor_mock')
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'valid@example.com', 'John Doe', 'password123')
        mock_connect.return_value = mock_connection

        response = self.app.post('/login', data={'email': 'valid@example.com', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 404)

    @patch('psycopg2.connect')
    def test_login_success(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_cursor = MagicMock(name='cursor_mock')
        mock_cursor.execute.return_value = None  # Mimic successful query execution
        mock_cursor.fetchone.return_value = (1, 'valid@example.com', 'John Doe', 'password123')  # Simulate valid user
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        response = self.app.post('/login', data={'email': 'valid@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)

    def test_signup_missing_fields(self):
        response = self.app.post('/signup')
        self.assertEqual(response.status_code, 401)

    @patch('psycopg2.connect')
    def test_signup_success(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_cursor = MagicMock(name='cursor_mock')
        mock_cursor.execute.return_value = None  # Mimic successful query execution
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        response = self.app.post('/signup', data={'email': 'new@example.com', 'name': 'New User', 'password': 'new_password'})
        self.assertEqual(response.status_code, 201)

    @patch('psycopg2.connect')
    def test_login(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_cursor = MagicMock(name='cursor_mock')
        mock_cursor.fetchone.return_value = None  # Simulate no user found
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        response = self.app.post('/login', data={'email': 'invalid@example.com', 'password': 'invalid_password'})
        self.assertEqual(response.status_code, 404)

    @patch('psycopg2.connect')
    def test_healthcheck_ok(self, mock_connect):
        mock_connection = MagicMock(name='connection_mock')
        mock_connect.return_value = mock_connection

        response = self.app.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok')

    @patch('psycopg2.connect')
    def test_healthcheck_error(self, mock_connect):
        mock_connect.side_effect = psycopg2.Error

        response = self.app.get('/healthcheck')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, b'error')

if __name__ == '__main__':
    unittest.main()
