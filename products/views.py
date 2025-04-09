from django.shortcuts import render
from django.views import View
from .models import Category,Product,ProductImage

#class base view for products pafe
class products(View):
    def get(self,request):
        context={
            'categories':Category.objects.all,
            'products':Product.objects.all,
            'productImaged':ProductImage.objects.all,
        }
        return render(request,'products/products.html',context)
#class base view for product page
class product(View):
    def get(self,request,pk):
        product=Product.objects.get(id=pk)
        context={
            'Product':product,
            'productImage':product.images.all,
            'category':product.category,
            'authonticated':request.user.is_authenticated,
        }
        return render(request,'products/product.html',context)

