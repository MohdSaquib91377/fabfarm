from django.db import models
from account.models import TimeStampModel,CustomUser
from store.models import Product

# Create your models here.
class Wishlist(TimeStampModel):
    product = models.ForeignKey("store.Product",related_name = "wishlist", on_delete = models.CASCADE)
    user = models.ForeignKey("account.CustomUser",related_name = "wishlist", on_delete = models.CASCADE)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.id}       ->          {self.user}"