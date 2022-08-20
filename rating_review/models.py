from django.db import models
from account.models import *
from store.models import *
from order.models import *
# Create your models here.
class Rating(TimeStampModel):
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "ratings") # who posted the reviews/rating
    order_item = models.ForeignKey(OrderItem, on_delete = models.CASCADE,related_name = "ratings",null=True,blank=True) # order item that was ratted by the user
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name = "ratings") #store the Product that the reviews/rating belongs to
    rating = models.IntegerField(default = 0) # where we will store the rating from 1 to 5
    comment = models.CharField(max_length = 64,null = True,blank = True) # will store the content of the comment of the reviews
    status = models.BooleanField(default = False) # Decide weather rating or review should published. we can prevent spam and fake review

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.user.fullname} {self.product.name} {self.rating}"

