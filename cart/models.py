from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
# Create your models here.
from store.models import Product
from account.models import CustomUser,TimeStampModel

class Cart(TimeStampModel):
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey('account.CustomUser',on_delete=models.CASCADE,null=True)
    total_price = models.FloatField(default=0)
    total_item = models.IntegerField(default=0)
    
class CartItem(TimeStampModel):
    cart = models.ForeignKey('Cart',related_name="cart_items",on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product',on_delete=models.CASCADE)
    price = models.IntegerField(default = 0)
    quantity = models.IntegerField()


@receiver(post_save, sender=CartItem)
def Calc_total_item_and_total_price(sender,**kwargs):
    cart_item_instance = kwargs['instance']
    product = Product.objects.filter(id = cart_item_instance.product_id).first()
    product_total_price = cart_item_instance.quantity * int(product.price)
    print("i got called")