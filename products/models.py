from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=150)
    id=models.AutoField(primary_key=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=150)
    description=models.CharField(max_length=3500)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to="image/")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to="image")

