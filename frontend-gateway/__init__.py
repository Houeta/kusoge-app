from flask import Flask
from flask_login import UserMixin  #Usermixin provides default user authentication methods

# Class that represents a user in the application, extending Usermixin 
class User(UserMixin):
    # Initialize the User object with ID, name, and active status
    def __init__(self, id,  name="", active=True):
        self.name = name
        self.id = id
        self.active = active # Whether the user is active
    
    # Method to check if the user is active 
    def is_active(self):
        return self.active # Return True if the user is active

    # MEthod to check if the user is anonymous (always False)
    def is_anonymous(self):
        return False
    
    def is_authenticated(self): # always True
        return True

def create_app():
    app = Flask(__name__)
    return app