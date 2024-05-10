import unittest
from unittest.mock import patch
from flask import Flask
import main

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = main.app.test_client()
    
    @patch('main.get_all_products')
    def test_get_products(self, mock_get_all_products):
        # Mocking get_all_products to return sample data
        mock_get_all_products.return_value = [
            main.Product(id=1, name='Product 1', description='Description 1', price=10.0),
            main.Product(id=2, name='Product 2', description='Description 2', price=20.0)
        ]
        response = self.app.get('/products')
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Product 1')
        self.assertEqual(data[1]['price'], 20.0)
        self.assertEqual(response.status_code, 200)
    
    @patch('main.create_product')
    def test_add_product(self, mock_create_product):
        # Mocking create_product
        response = self.app.post('/products', data={'name': 'New Product', 'description': 'New Description', 'price': 30.0})
        mock_create_product.assert_called_once_with('New Product', 'New Description', '30.0')
        self.assertEqual(response.status_code, 200)
    
    @patch('main.update_product')
    def test_update_product_put(self, mock_update_product):
        # Mocking update_product
        response = self.app.put('/products/1', data={'name': 'Updated Product', 'price': 40.0})
        mock_update_product.assert_called_once_with(1, {'name': 'Updated Product', 'price': '40.0', 'description': None})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()