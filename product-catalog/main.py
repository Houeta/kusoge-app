from os import getenv

from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ENV VARIABLES
db_host = getenv('PG_HOST', 'localhost')
db_password = getenv('PG_PASSWORD', 'example')
db_user = getenv('PG_USER', 'kusoge')
db_name = getenv('PG_DB_NAME', 'KUSOGE_SHOP')
db_table_name = getenv('PG_PRODUCT_TABLE', 'products')


Base = declarative_base()

class Product(Base):
    __tablename__ = db_table_name
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
    query = session.query(Product).all()
    return query
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
    return jsonify([product.as_dict() for product in products])

@app.route('/products', methods=['POST'])
def add_product():
    create_product(request.form.get('name'), request.form.get('description'), request.form.get('price'))
    return jsonify({'message': 'Product created successfully'}), 200

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = {
        'name': request.form.get('name'),
        'description': request.form.get('description') if request.form.get('description') else None,
        'price': request.form.get('price')
    }
    update_product(product_id, data)
    return jsonify({'message': 'Product updated succesfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    delete_product(product_id)
    return jsonify({'message': {'Product deleted succesfully'}})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')