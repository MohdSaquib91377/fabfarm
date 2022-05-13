from django.db import models
# Create your models here.
from store.models import Product
from account.models import CustomUser,TimeStampModel

class Cart(TimeStampModel):
    user = models.ForeignKey('account.CustomUser',on_delete=models.CASCADE,null=True)
    product = models.ForeignKey('store.Product',on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-id']

    @staticmethod
    def get_cart_total_item_or_cost(user):
        carts = Cart.objects.filter(user=user)
        cart_total = 0
        cart_item = 0
        for cart in carts:
            cart_total = cart_total + int(cart.quantity) * int(cart.product.price)
            cart_item = cart_item + int(cart.quantity) 
        return cart_total,cart_item

    