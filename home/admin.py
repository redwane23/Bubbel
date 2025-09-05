from django.contrib import admin
from .models import  CustomUser,Cart,CartItem,WishList,WishListItem,order_list

admin.site.register(CustomUser)

admin.site.register(Cart)

admin.site.register(CartItem)
 
admin.site.register(WishList)

admin.site.register(WishListItem)

admin.site.register(order_list)

