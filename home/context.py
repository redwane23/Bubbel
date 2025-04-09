# send data to all views so i dont have to repeatly send in every view
from .models import Card,CardItem,WishList,WishListItem

def context_global(request):
    if request.user.is_authenticated:
        card=Card.objects.get(owner=request.user)
        whishlist=WishList.objects.get(owner=request.user)
        newcard=CardItem.objects.filter(card=card)
        if not newcard:
            empty=False
        else:
            empty=True
        return{
            'user':request.user,
            'card':card,
            'CartItems':CardItem.objects.filter(card=card),
            'whishlist':whishlist,
            'wishlistitem':WishListItem.objects.filter(wishlist=whishlist),
            'is_authenticated':request.user.is_authenticated,
            'is_empty':empty,
        }
    else:
        return{
            'is_authenticated':request.user.is_authenticated,
        }