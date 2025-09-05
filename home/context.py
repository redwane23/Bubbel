# send data to all views so i dont have to repeatly send in every view
from .models import Cart,CartItem,WishList,WishListItem

def context_global(request):
    if request.user.is_authenticated:
        cart=Cart.objects.get(owner=request.user)
        whishlist=WishList.objects.get(owner=request.user)
        newcart=CartItem.objects.filter(cart=cart)
        if not newcart:
            empty=False
        else:
            empty=True
        return{
            'user':request.user,
            'cart':cart,
            'CartItems':CartItem.objects.filter(cart=cart),
            'whishlist':whishlist,
            'wishlistitem':WishListItem.objects.filter(wishlist=whishlist),
            'is_authenticated':request.user.is_authenticated,
        }
    else:
        return{
            'is_authenticated':request.user.is_authenticated,
        }