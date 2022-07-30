from email import message
from operator import le
from pyexpat import model
from django.db import models
from account.models import CustomUser,TimeStampModel
from store.models import *
from coupon.models import *
# Create your models here.

class Order(TimeStampModel):

    payment_choices = (

        ("payment_failed","payment failed"),
        ("payment_success","payment success"),
        ("payment_pending","payment pending"),
        ("partial_payment_refund_in_progress", "Partial Payment Refund In Progress"),
        ("payment_refund_full", "Payment Refund Full"),
        ("payment_refund_partial", "Payment Refund Partial"),

        )

    order_choises = (
        
        ("order_cancelled","order cancelled"),
        ("order_pending","order pending"),
        ("order_success","order success"),
        ("partial_order_in_progress","partial order in progress"),
        ("partial_order","partial_order"),
        ("partial_refund_failed","partial refund failed")

    )
    user = models.ForeignKey('account.CustomUser',on_delete = models.CASCADE,related_name = "orders")
    full_name = models.CharField(max_length=24)
    city = models.CharField(max_length=24)
    state = models.CharField(max_length=24)
    country = models.CharField(max_length = 24)
    pincode = models.IntegerField()
    locality = models.CharField(max_length = 64)
    landmark = models.CharField(max_length = 64,null = True)
    address = models.TextField()
    alternate_number = models.BigIntegerField()
    total_price = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=64,null = True)
    payment_id = models.CharField(max_length=64,null=True)
    message = models.TextField(null = True)
    tracking_no = models.CharField(max_length=64,null = True)
    order_status = models.CharField(choices = order_choises,default = "order_pending",max_length = 64)
    
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
    payment_status = models.CharField(choices = payment_choices,default = "payment_pending",max_length = 64)

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
        ("Delivered","Delivered"),
        ("refund_in_progress","Refund In Progress"),
        ("Refund","Refund"),
        ("refund_failed","Refund Failed"),

        )

    status = models.CharField(choices=order_status,default = "Pendding",max_length = 64)

    def __str__(self):
        return f"{self.order.id} -  {self.order.tracking_no}"

    def save(self, *args, **kwargs):
        total_order_item = OrderItem.objects.filter(order_id = self.order.id)
        deliver_item = OrderItem.objects.filter(status__in = ["Delivered"])
        if total_order_item.count() == deliver_item.count():
            order = Order.objects.filter(id = self.order.id).update(order_status = "order_success")
        super(OrderItem, self).save(*args, **kwargs)