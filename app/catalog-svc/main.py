from os import getenv

from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ENV VARIABLES
db_host = getenv('PG_HOST')
db_password = getenv('POSTGRES_PASSWORD')
db_user = getenv('POSTGRES_USER')
db_name = getenv('POSTGRES_DB')
db_table_name = getenv('PG_PRODUCT_TABLE')

# Declare a base class for SQLAlchemy models
Base = declarative_base()

# Define the Product class as a model for the product table
class Product(Base):
    __tablename__ = db_table_name # Table name int DB
    
    id = Column(Integer, primary_key=True) # primary key
    name = Column(String, nullable=False)  # required
    description = Column(String)           # optional
    price = Column(Float, nullable=False)  # required
    
    # Method to return product data as a dictionary
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Initialize the connection to the PostgreSQL database
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
Session = sessionmaker(bind=engine)
session = Session() # Create a new database session

## CRUD realization
# Function to create a new product
def create_product(name, description, price):
    new_product = Product(name=name, description=description, price=price)
    session.add(new_product)
    session.commit()
# Funtion to get all products from the DB
def get_all_products():
    query = session.query(Product).all() # query all products from the DB
    return query
# Function to update a product's
def update_product(product_id, new_data):
    product = session.query(Product).get(product_id) # Retrieve the product by ID
    if product:
        # Update the product with the new data
        for k, v in new_data.items():
            setattr(product, k, v)
        session.commit() # Commit the changes to the DB
# Function to delete a product by ID
def delete_product(product_id):
    product = session.query(Product).get(product_id)
    if product:
        session.delete(product)
        session.commit()

# Initialize the Flask application    
app = Flask(__name__)

# Route to retrieve all products as a JSON response
@app.route('/products', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify([product.as_dict() for product in products])

# Route to add a new product to the DB
@app.route('/products', methods=['POST'])
def add_product():
    create_product(request.form.get('name'), request.form.get('description'), request.form.get('price'))
    return jsonify({'message': 'Product created successfully'}), 200

# Route to update a product by ID with new data 
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_put(product_id):
    # Gather data to update the product
    data = {
        'name': request.form.get('name'), 
        'description': request.form.get('description') if request.form.get('description') else None,
        'price': request.form.get('price')
    }
    # Update the product with the new data
    update_product(product_id, data)
    return jsonify({'message': 'Product updated succesfully'})

# Route to delete a product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    delete_product(product_id) 
    return jsonify({'message': {'Product deleted succesfully'}})

# Start the Flask application with debugging enabled
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')