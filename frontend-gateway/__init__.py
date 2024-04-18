from flask import Flask
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id,  name="", active=True):
        self.name = name
        self.id = id
        self.active = active
    
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True

def create_app():
    app = Flask(__name__)
    return app