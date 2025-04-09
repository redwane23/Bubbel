from django.contrib import admin
from .models import Category,Product,ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name')
    search_field=('name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','description','price','image','category')
    search_field=('id')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=('product','image')
