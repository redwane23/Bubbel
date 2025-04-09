from itertools import product
import string
from products.models import Product
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings

class CustomUserManeger(BaseUserManager):
    #account creationg managment
    def create_user(self,email,Username,password,**other_fields):

        email=self.normalize_email(email)
        user=self.model(email=email,Username=Username,is_active=True,**other_fields)

        user.set_password(password)
        user.save()

        return user
    def create_superuser(self,email,Username,password,**other_fields):

        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("superuser must be assigned to is_staff=True")
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError("superuser must be assigned to is_superuser=True")

        return self.create_user(email,Username,password,**other_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    # custom user model 
    Username=models.CharField(max_length=150,unique=True)
    email=models.EmailField(unique=True)
    date_join=models.DateTimeField(auto_now_add=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    objects=CustomUserManeger()

    USERNAME_FIELD="Username"
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.Username


class Card(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owner')

    def price_to_pay(self):
        return  sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Owned by {self.owner}" 

class CardItem(models.Model):
    card=models.ForeignKey(Card,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='item')
    quantity=models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
        
    def __str__(self):
        return self.product.name


class WishList(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='theowner')
    def __str__(self):
        return f'owend by {self.owner}'


class WishListItem(models.Model):
    wishlist=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name='products')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')

    def __str__(self):
        return self.product.name

class order_list(models.Model):
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    data=models.JSONField()
