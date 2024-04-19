from os import getenv

from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ENV VARIABLES
db_host = getenv('PG_HOST')
db_password = getenv('PG_PASSWORD')
db_user = getenv('PG_USER')
db_name = getenv('PG_DB_NAME')
db_table_name = getenv('PG_PRODUCT_TABLE')


Base = declarative_base()

class Product(Base):
    __tablename__ = db_table_name
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric, nullable=False)

# Init to postgres
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
Session = sessionmaker(bind=engine)
session = Session()

# CRUD realization
def create_product(name, description, price):
    new_product = Product(name=name, description=description, price=price)
    session.add(new_product)
    session.commit()

def get_all_products():
    return session.query(Product).all()

def update_product(product_id, new_data):
    product = session.query(Product).get(product_id)
    if product:
        for k, v in new_data.items():
            setattr(product, k, v)
        session.commit()

def delete_product(product_id):
    product = session.query(Product).get(product_id)
    if product:
        session.delete(product)
        session.commit()
        
app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    products = get_all_products()
    print(products)
    return jsonify({key:value for key, value in products})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    create_product(data['name'], data['description'], data['[price]'])
    return jsonify({'message': 'Product created successfully'}), 200

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    update_product(product_id, data)
    return jsonify({'message': 'Product updated succesfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    delete_product(product_id)
    return jsonify({'message': {'Product deleted succesfully'}})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')