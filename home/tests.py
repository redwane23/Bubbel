from django.test import TestCase
from django.contrib.auth import get_user_model 
from .forms import JoinForm, LoginForm
from .models import Cart,CartItem,WishList,WishListItem
from products.models import Product,Category
User=get_user_model()

class HomeViewsTests(TestCase):

    def test_home_view_status_code(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.view_name, 'home')

    def test_join_view_post_success(self):
        response = self.client.post('/home/join/', {
            'Username': 'testuser',
            'password1': 'testpass123',
            'email':'test_email@gmail.com',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertEqual(response.url,'/home/')  # Redirects to home
        self.assertTrue(User.objects.filter(Username="testuser").exists()) # User is created


    def test_join_view_post_failed(self):
        response = self.client.post('/home/join/', {
            'username': '',
            'password1': 'testpass123',
            'email':'bad_email',
            'password2': 'not_the_same'
        })
        self.assertEqual(response.status_code,200)  # Renders form again on failure
        self.assertEqual(response.resolver_match.view_name, 'join')
        self.assertIsInstance(response.context["form"], JoinForm)
        self.assertTrue(response.context['form'].errors.as_json())  # Form has errors 

    def test_login_view_success(self):
        User.objects.create_user(Username="testuser", password="testpass123",email='test@gmail.com')
        self.assertTrue(User.objects.filter(Username="testuser").exists()) # User is created

        response = self.client.post('/home/login/',{
            'username':'testuser',
            'password':'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,'/home/') 
    
    def test_login_view_failed(self):
        response = self.client.post('/home/login/',{
            'username':'nonexistent',
            'password':'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Renders form again on failure
        self.assertEqual(response.resolver_match.view_name, 'login')
        self.assertIsInstance(response.context["form"], LoginForm)


    def test_cart_view_status_code(self):
        response = self.client.get('/home/Cart')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        User.objects.create_user(Username="testuser", password="testpass123",email="test@email.com")
        self.client.login(Username="testuser", password="testpass123")
        response = self.client.get('/home/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,'/home/')
    
class HomeModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(Username="testuser", password="testpass123", email="test@email.com")
        cls.test_category = Category.objects.create(name="Test Category")
        cls.test_product = Product.objects.create(name="Test Product", description="A product for testing", price=10.00,category=cls.test_category, image=f"/static/Home/images/1721418270319.jpg")
        cls.test_cart =Cart.objects.get(owner=cls.test_user)
        cls.test_cart_item=CartItem.objects.create(cart=cls.test_cart,product=cls.test_product,quantity=2)
        cls.test_wishlist=WishList.objects.get(owner=cls.test_user)
        cls.test_wishlistItem=WishListItem.objects.create(wishlist=cls.test_wishlist,product=cls.test_product)

    def test_Cart_model(self):
        self.test_cart.items.add(self.test_cart_item)
        self.assertEqual(self.test_cart.price_to_pay(),20.00)
        self.assertEqual(str(self.test_cart),f"Owned by {self.test_user}")
    
    def test_CartItem_model(self):
        self.assertEqual(self.test_cart_item.total_price(),20.00)
        self.assertEqual(str(self.test_cart_item),self.test_product.name)

    def test_whishlist_model(self):
        self.assertEqual(str(self.test_wishlist),f"owend by {self.test_user}")
    
    def test_whishlistitem_model(self):
        self.assertEqual(str(self.test_wishlistItem),self.test_product.name)