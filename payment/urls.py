from django.urls import path
from .views import CreateCheckoutSessionView,payment_success,payment_faild

urlpatterns = [
    path('create-checkout-session/<int:order_id>/', CreateCheckoutSessionView, name='create-checkout-session'),
    path("payment/success/<int:order_id>/", payment_success, name="payment-success"),
    path("payment/faild/<int:order_id>/", payment_faild, name="payment-faild"),

]