from home.models import *
from products.models import Product
import json
from django.shortcuts import redirect
from django.http import JsonResponse
from home.signals import called
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

@login_required
def updated_quantity(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        itemID =data.get('id')
        action=data.get("action")  

        # Check if the action is valid
        allowed_actions = {"increase", "decrease", "Remove"}
        if action not in allowed_actions:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
        
        owner=request.user
        cart=Cart.objects.get(owner=owner)

        item = next((cartitem for cartitem in cart.items.all() if cartitem.id == itemID), None)
        if item is None:
            return JsonResponse({'status':'faild','reason':'item does not exist'})

        if action=='increase':
            item.quantity+=1
            item.save()
        elif action=='decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        elif action=='Remove':
            item.delete()
            new_price_to_pay=cart.price_to_pay()
            return JsonResponse({'status':'item has been removed','new_price_to_pay':new_price_to_pay,})
        
        new_total_item_price=item.total_price()
        new_price_to_pay=cart.price_to_pay()
        
        return JsonResponse({
            'status':"quantity updated",
            'new_quantity':item.quantity,
            'new_price_to_pay':new_price_to_pay,
            'new_total_item_price':new_total_item_price,
        })
    except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def AddToCart(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        id = data.get('id')

        newitem = Product.objects.get(id=id)
        owner = request.user
        cart = Cart.objects.get(owner=owner)
        cartitems = CartItem.objects.select_related("product").filter(cart=cart).only('product__name')

        for item in cartitems:
            if item.product.name == newitem.name:
                return JsonResponse({'status': 'failed', 'reason': "Item already exists"})

        newcartitem = CartItem.objects.create(cart=cart, product=newitem)
        newcartitem.save()

        return JsonResponse({"status": 'Item has been added successfully'})
    
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart not found'}, status=404)

        


@login_required
def getCartItem(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        owner=request.user
        cart=Cart.objects.get(owner=owner)
        items=CartItem.objects.select_related("product").filter(cart=cart)

        itemsdata=[]

        for item in items:
            itemsdata.append({
                'id':item.id,
                'cart':str(item.cart),
                'product':item.product.name,
                'quantity':int(item.quantity),
                'total_price':float(item.total_price()),
            })
        return JsonResponse({
            'itemsdata':itemsdata,
            'status':"success",
        })
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart not found'}, status=404)
    except Exception as e:      
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



class WishListItems(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):

            wishlist=WishList.objects.get(owner=request.user)
            items = WishListItem.objects.select_related("product").filter(wishlist=wishlist).only('product__name')

            itemsdata = [{"id": item.id, "product": item.product.name} for item in items]
            return JsonResponse({
                'itemsdata':itemsdata,
                'status':"success",
            })
    
    def post(self, request):
        try:
            data = request.data  
            item_id = data.get("id")

            wishlist = WishList.objects.get(owner=request.user)
            newitem = Product.objects.get(id=item_id)

            if WishListItem.objects.filter(wishlist=wishlist, product=newitem).exists():
                return JsonResponse({"status": "failed", "reason": "Already exists"}, status=400)

            WishListItem.objects.create(wishlist=wishlist, product=newitem)
            return JsonResponse({"status": "success", "message": "Item has been added successfully"}, status=201)

        except Product.DoesNotExist:
            return JsonResponse({"status": "failed", "reason": "Product does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "failed", "reason": str(e)}, status=500)


@login_required
def DeletWishListItem(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        data=json.loads(request.body)

        itemid=data.get('itemid')

        wishlistitem=WishListItem.objects.get(id=itemid)

        wishlistitem.delete()

        return JsonResponse({'status':'deleted susscefully'})
    except WishListItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)



#cleaer the cart and send an email that contain the the order informations
def ordered(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        owner=request.user
        cart=Cart.objects.get(owner=owner)
        items=CartItem.objects.filter(cart=cart)
        if items.count()==0:
            return JsonResponse({'status':'faild','reason':'the cart is empty'})
        order=[]
        for item in items:
            singal_order={ str(item) : item.quantity}
            order.append(singal_order)

        total_price=cart.price_to_pay()
        new_order=order_list.objects.create(customer=owner,data=order,totla_cost=total_price)

        cart.items.all().delete()
        called.send(sender='ordered',message=order,user_id=owner.id) 
    
        return redirect(f'/payment/create-checkout-session/{new_order.id}')


    except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart not found'}, status=404)
    except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


