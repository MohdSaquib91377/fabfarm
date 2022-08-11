from email import message
from operator import le
from pyexpat import model
from django.db import models
from account.models import CustomUser,TimeStampModel,UserAddress
from store.models import *
from coupon.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.

class Order(TimeStampModel):

    payment_choices = (

        ("payment failed","payment failed"),
        ("payment success","payment success"),
        ("payment pending","payment pending"),
        ("Partial Payment Refund In Progress", "Partial Payment Refund In Progress"),
        ("Payment Refund Full", "Payment Refund Full"),
        ("Payment Refund Partial", "Payment Refund Partial"),

        )

    order_choises = (
        
        ("order cancelled","order cancelled"),
        ("order pending","order pending"),
        ("order success","order success"),
        ("partial order in progress","partial order in progress"),
        ("partial order","partial order"),
        ("partial refund failed","partial refund failed")

    )
    user = models.ForeignKey('account.CustomUser',on_delete = models.CASCADE,related_name = "orders")
    user_address = models.ForeignKey(UserAddress,on_delete = models.SET_NULL,null = True)
    # full_name = models.CharField(max_length=24)
    # city = models.CharField(max_length=24)
    # state = models.CharField(max_length=24)
    # country = models.CharField(max_length = 24)
    # pincode = models.IntegerField()
    # locality = models.CharField(max_length = 64)
    # landmark = models.CharField(max_length = 64,null = True)
    # address = models.TextField()
    # alternate_number = models.BigIntegerField()
    total_price = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=64,null = True)
    payment_id = models.CharField(max_length=64,null=True)
    # message = models.TextField(null = True)
    tracking_no = models.CharField(max_length=64,null = True)
    order_status = models.CharField(choices = order_choises,default = "order pending",max_length = 64)
    
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
    payment_status = models.CharField(choices = payment_choices,default = "payment pending",max_length = 64)

    def __str__(self):
        return f"{self.id}"



class OrderItem(TimeStampModel):
    order = models.ForeignKey('Order',on_delete=models.CASCADE,related_name="orderItem")
    product = models.ForeignKey('store.Product',on_delete = models.CASCADE,related_name="orderItem")
    price = models.FloatField(null = True)
    quantity = models.IntegerField(null = True)
    order_status = (   
          
        ("Pending","Pending"),
        ("Out For Shipping","Out For Shipping"),
        ("Completed","Completed"),
        ("Packed","Packed"),
        ("Cancelled","Cancelled"),
        ("Delivered","Delivered"),
        ("Refund In Progress","Refund In Progress"),
        ("Refunded","Refunded"),
        ("Refund Failed","Refund Failed"),
        ("Request Refund","Request Refund")

        )

    status = models.CharField(choices=order_status,default = "Pending",max_length = 64)
    make_refund = models.CharField(max_length = 64,null = True, blank = True)

    def __str__(self):
        return f"{self.order.id} -  {self.order.tracking_no}"
    
    def make_refund(self):
        if self.status in ["Request Refund"]:
            url = reverse("admin-refund")
            return format_html("<a href='%s'>%s</a>" % (url, "Refund"))



    class Meta:
        ordering = ["-id"]

@receiver(post_save, sender=OrderItem)
def make_order_success(sender, instance, **kwargs):
    order_item = OrderItem.objects.filter(order_id = instance.order.id)
    deliver_item = OrderItem.objects.filter(status__in=["Delivered"],order_id = instance.order.id)
    if order_item.count() == deliver_item.count():
        Order.objects.filter(id = instance.order.id).update(order_status="order success")

    