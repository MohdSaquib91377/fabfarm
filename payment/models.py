from distutils.log import error
from account.models import TimeStampModel,CustomUser
from order.models import Order
from django.db import models

class Payment(TimeStampModel):
    order = models.ForeignKey(Order, related_name="payment",on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="payment",on_delete = models.CASCADE)

    # payment successful
    razorpay_payment_id = models.CharField(max_length=64)
    razorpay_order_id = models.CharField(max_length=64)
    razorpay_signature = models.CharField(max_length= 64)
    method = models.CharField(max_length=64)
    fee = models.CharField(max_length=64)
    tax = models.CharField(max_length=64)

    # payment Errors
    error_code = models.TextField(max_length=64,null=True,blank=True)
    error_description = models.TextField(max_length=64,null=True,blank=True)
    error_source = models.TextField(max_length=64,null=True,blank=True)
    error_step = models.TextField(max_length=64,null=True,blank=True)
    error_reason = models.CharField(max_length=64,null=True,blank=True)
    error_order_id = models.TextField(max_length=64,null=True,blank=True)
    error_payment_id = models.TextField(max_length=64,null=True,blank=True)

    class Meta:
        db_table = 'Payments'