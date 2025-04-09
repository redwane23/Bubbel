from django.contrib import admin
from .models import  CustomUser,Card,CardItem,WishList,WishListItem,order_list

admin.site.register(CustomUser)

admin.site.register(Card)

admin.site.register(CardItem)
 
admin.site.register(WishList)

admin.site.register(WishListItem)

admin.site.register(order_list)

