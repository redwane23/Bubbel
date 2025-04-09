from django.urls import path
from . import views
urlpatterns = [
    path("",views.products.as_view(),name='products'),
    path("product/<int:pk>/",views.product.as_view(),name='product'),#send an pk to determine the chosen product

]