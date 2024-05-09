from os import getenv

from flask import Flask, request
import psycopg2

# Initialize Flask application
app = Flask(__name__)

# Function to establish a connect with a PostrgeSQL database
def _get_db_connection():
    conn = psycopg2.connect( # Connect to the postgres db
        host=getenv('PG_HOST'),
        database=getenv('PG_DB_NAME'),
        user = getenv('PG_USER'),
        password=getenv('PG_PASSWORD'),
        port=5432 # Default postgres port
    )
    return conn # return the db connection

# Rout to handle use rlogin (POST)
@app.route('/login', methods=['POST'])
def login():
    auth_table = getenv('PG_AUTH_TABLE') # Table name for authentication data
    # collect login credentials from the request
    auth = {
        'email': request.form.get('email'),
        'password': request.form.get('password')
    }
    # If any required fields are missing, return an error message with status code 401
    if not auth or not auth['email'] or not auth['password']: 
        return "Couldn't verify! You have empty fields.", 401
    
    # Establish a connection to the DB and create a cursor for execution queries
    conn = _get_db_connection()
    cursor = conn.cursor()
    # Query to retrieve user data bassed on the provided email
    query = f'SELECT id, email, name, password FROM {auth_table} WHERE email = %s'
    result = cursor.execute(query, (auth['email'],))
    
    if result is None:
        # Fetch the result
        user_credentials = cursor.fetchone()
        # If no user is found with the provided email, return a 404 status code with an error
        if user_credentials is None:
            return "Email address doesn't exist", 404
        
        # Check if the prvided email and pass match the retrieved credentials
        if auth['email'] != user_credentials[1] or auth['password'] != user_credentials[3]:
            return "Couldn't verify. Incorrect email or password", 404
        else:
            # If the credentials match, return the user's ID and name as a response
            result = f"{user_credentials[0]}:{user_credentials[2]}"
            return result, 200
    else:
        return "Couldn't verify. Incorrect email or password", 404

# Route to handle user signup (POST)
@app.route('/signup', methods=['POST'])
def signup():
    auth_table = getenv('PG_AUTH_TABLE')
    data = {
        'email': request.form.get('email'),
        'name': request.form.get('name'),
        'password': request.form.get('password')
    }
    if not data or not data['email'] or not data['password'] or not data['name']: 
        return "Couldn't verify! You have empty fields.", 401
    
    # Esatblish a DB connection and create a cursor
    conn = _get_db_connection()
    cursor = conn.cursor()
    # Insert the new user into the auth table
    query = f'INSERT INTO {auth_table}(email, name, password) VALUES(%s, %s, %s) RETURNING *'
    result = cursor.execute(query, (data['email'], data['name'], data['password'])) # Execute query
    conn.commit() # Commit the transaction to make the changes persistent
    if result is None:
        return f"Success", 201 # Return status code 201 (Created) indicating a successful signup

# Start the Flask application when run as a script
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)