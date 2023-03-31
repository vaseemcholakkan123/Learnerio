from django.dispatch import receiver
from django.db.models.signals import post_save
from User.models import User,Wishlist,Cart

# @receiver(post_save,sender = User)
# def CreateCartAndWishlist(sender,instance,*args,**kwargs):

#     user_wishlist = Wishlist.objects.create(user_id=instance)
#     user_cart = Cart.objects.create(user_id=instance)
#     print("Signal called")
#     user_cart.save()
#     user_wishlist.save()
