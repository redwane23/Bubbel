from django.urls import path
from . import views

urlpatterns = [
    path("update-quantity/",views.updated_quantity),
    path("AddToCart/",views.AddToCart),
    path("getCartItem/",views.getCartItem),
    path("AddToWishlist/",views.WishListItems.as_view()),
    path("getWishlistItem/",views.WishListItems.as_view()),
    path("DeletWishListItem/",views.DeletWishListItem),
    path("ordered/",views.ordered),
]
