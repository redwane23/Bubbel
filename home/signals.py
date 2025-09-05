from .models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver,Signal
from django.conf import settings
from .models import Cart,WishList
from django.core.mail import send_mail

called=Signal() #custom signal when a fuction called

#create a cart whenever Custom user created
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_card(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(owner=instance)

#create a whishlist whenever Custom user created
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_card(sender,instance,created,**kwargs):
    if created:
        WishList.objects.create(owner=instance)

#send an email to the customer  when he order
@receiver(called)
def SendEmail(sender, **kwargs):

    user_id=kwargs.get('user_id')
    order=kwargs.get("message")
    user=CustomUser.objects.get(id=user_id)
    user_email=user.email

    print(send_mail(
    "update about your cart", 
    f"""hello {user} your order hava been sent succsufuly
    thx for Using our servive
    you orderd{order}  
    """, # message
    settings.EMAIL_HOST_USER, # from email
    [user_email], 
    fail_silently=False, 
    ))
