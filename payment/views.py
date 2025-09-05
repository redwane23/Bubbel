import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import  get_object_or_404
from home.models import order_list
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY


def CreateCheckoutSessionView(request, order_id):
        order = order_list.objects.get(id=order_id, customer=request.user)
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Order #{order.id}"
                            },
                        'unit_amount': int(order.totla_cost * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + f'/payment/payment/success/{order.id}/',
            cancel_url=YOUR_DOMAIN + f'/payment/payment/faild/{order.id}/',


        )
        print(checkout_session.url)
        return redirect(checkout_session.url)

def payment_success(request, order_id):
    order = order_list.objects.get(id=order_id, customer=request.user)
    
    # Retrieve the latest session for this order
    checkout_sessions = stripe.checkout.Session.list(
        limit=1,
        payment_intent=order.stripe_payment_intent  if hasattr(order, "stripe_payment_intent") else None
    )

    if checkout_sessions.data:
        session = checkout_sessions.data[0]
        if session.payment_status == "paid":
            # order.paid = True
            # order.save()
            msg = "✅ Payment successful!"
        else:
            msg = "⚠️ Payment not completed."
    else:
        msg = "⚠️ Could not verify payment."
    print({"order": order, "message": msg})
    return HttpResponse(msg)
    return render(request, "payment/success.html", {"order": order, "message": msg})
def payment_faild(request, order_id):
    order = order_list.objects.get(id=order_id, customer=request.user)
    msg = "❌ Payment failed or was canceled."
    return HttpResponse(msg)
    return render(request, "payment/faild.html", {"order": order, "message": msg})  