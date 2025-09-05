from django.urls import path

from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('Cart',views.CartView,name='Cart'),
    path('join/',views.join,name='join'),
    path('login/',views.custom_login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
]