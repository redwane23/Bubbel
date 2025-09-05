from django.test import TestCase
from django.contrib.auth import get_user_model
from home.models import Cart, CartItem
from products.models import Product,Category
from django.urls import reverse
import json

User = get_user_model()

class APITVieweTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(Username='testuser', password='testpass' ,email='test@gmail.com')
        self.category = Category.objects.create(name='Category 1')
        self.product1 = Product.objects.create(name='Product 1', price=10.0,category=self.category)
        self.product2 = Product.objects.create(name='Product 2', price=20.0,category=self.category)
        self.cart = Cart.objects.get(owner=self.user)
        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('AddToCart'), data=json.dumps({"id": self.product1.id}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'failed', 'reason': 'Item already exists'})

        response = self.client.post("/api/AddToCart/",{'id':self.product2.id}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'failed', 'reason': 'Item already exists'})

        new_product = Product.objects.create(name='Product 3', price=30.0,category=self.category)
        response = self.client.post("/api/AddToCart/",data=json.dumps({"id": 3}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'Item has been added successfully'})
        self.assertTrue(CartItem.objects.filter(cart=self.cart, product=new_product).exists())

    def test_get_cart_items(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('getCartItem'))
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'items': [
                {
                    'id': self.cart_item1.id,
                    'cart': str(self.cart),
                    'product': 'Product 1',
                    'quantity': 2,
                    'total_price': 20.0
                },
                {
                    'id': self.cart_item2.id,
                    'cart': str(self.cart),
                    'product': 'Product 2',
                    'quantity': 1,
                    'total_price': 20.0
                },
                ]
        }
        self.assertJSONEqual(response.content, {'itemsdata': expected_data['items'], 'status': 'success'})

