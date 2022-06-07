from email import message
from operator import le
from pyexpat import model
from django.db import models
from account.models import CustomUser,TimeStampModel
from store.models import *
from coupon.models import *
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
    # Coupon
    coupon = models.ForeignKey('coupon.Coupon',on_delete = models.CASCADE,related_name="order",null = True)
    discounted_price = models.FloatField(default = 0)
    total_amount_payble = models.FloatField(default = 0)
    # razorpay Details
    razorpay_order_id = models.CharField(max_length=64,null = True,blank = True)
    razorpay_status = models.CharField(max_length=16,null = True,blank = True)
    amount_due = models.PositiveBigIntegerField(default = 0,null = True,blank = True)
    amount_paid = models.PositiveBigIntegerField(default = 0,null = True,blank = True)
    attempts = models.PositiveIntegerField(default=0, blank=True, null=True)


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
