from email import message
from operator import le
from pyexpat import model
from django.db import models
from numpy import product
from account.models import CustomUser,TimeStampModel
from store.models import *
# Create your models here.

class Order(TimeStampModel):
    user = models.ForeignKey('account.CustomUser',on_delete = models.CASCADE,related_name = "orders")
    full_name = models.CharField(max_length=24)
    city = models.CharField(max_length=24)
    state = models.CharField(max_length=24)
    country = models.CharField(max_length = 24)
    pincode = models.IntegerField()
    locality = models.CharField(max_length = 64)
    landmark = models.CharField(max_length = 64,null = True)
    address = models.TextField()
    alternate_number = models.IntegerField()
    total_price = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=64,null = True)
    payment_id = models.CharField(max_length=64,null=True)
    message = models.TextField(null = True)
    tracking_no = models.CharField(max_length=64,null = True)

    def __str__(self):
            return f"{self.id}"


class OrderItem(TimeStampModel):
    order = models.ForeignKey('Order',on_delete=models.CASCADE,related_name="orderItem")
    product = models.ForeignKey('store.Product',on_delete = models.CASCADE,related_name="orderItem")
    price = models.FloatField(null = True)
    quantity = models.IntegerField(null = True)
    order_status = (     
        ("Pending","Pending"),
        ("Out For Shipping","Out For Shiping"),
        ("Completed","Completed"),
        ("Packed","Packed"),
        ("Cancel","Cancel"),

        )
    status = models.CharField(choices=order_status,default = "Pendding",max_length = 64)

    def __str__(self):
        return f"{self.order.id} -  {self.order.tracking_no}"
