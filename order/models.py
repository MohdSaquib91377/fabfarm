from email import message
from operator import le
from pyexpat import model
from django.db import models
from account.models import CustomUser,TimeStampModel,UserAddress
from store.models import *
from coupon.models import *
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Sum
from account.models import *

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
    is_return = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.id}"
    
    def make_refund(self):
        if self.status in ["Request Refund"] and self.order.payment_mode in ["razor_pay"]:
            url = reverse("admin-refund")
            return format_html("<a href='%s'>%s</a>" % (url, "Refund"))



    class Meta:
        ordering = ["-id"]

@receiver(post_save, sender=OrderItem)
def make_order_success(sender, instance, **kwargs):
    order_item = OrderItem.objects.filter(order_id = instance.order.id)
    deliver_item = OrderItem.objects.filter(status__in=["Delivered"],order_id = instance.order.id)
    if order_item.count() == deliver_item.count():
        Order.objects.filter(id = instance.order.id).update(order_status="order success",payment_status = "payment success")



class ReturnRefundPolicy(TimeStampModel):
    RETURN_REFUND_POLICY_CHOICES = (
        ("7 days","7 days"),
        ("14 days","14 days"),
        ("30 days","30 days"),
        ("45 days","45 days")

    )
    return_refund_timestamp = models.CharField(max_length = 16,choices = RETURN_REFUND_POLICY_CHOICES,default = '7 days')
    def __str__(self):
        return f"{self.return_refund_timestamp}"

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Return Refund Policy"

class ReceiveReturn(TimeStampModel):
    order_item = models.ForeignKey(OrderItem,on_delete = models.CASCADE,related_name = "receive_return")
    order = models.ForeignKey(Order,on_delete = models.CASCADE,related_name = "receive_return")
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name = "receive_return")

    def __str__(self):
        return f"{self.order_item.id} - {self.order.id} - {self.product.id}"
    
    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Receive Return"
    
@receiver(post_save, sender = OrderItem)
def create_receive_return(sender,instance,created,*args,**kwargs):
    if instance.is_return == True:
        obj, created = ReceiveReturn.objects.get_or_create(
            order_item=instance,
            order=instance.order,
            product=instance.product
        )

    else:
        if ReceiveReturn.objects.filter(order_item = instance).exists():
            ReceiveReturn.objects.filter(order_item = instance).delete()



class RequestRefundItem(TimeStampModel):
    order_item = models.ForeignKey(OrderItem,on_delete = models.CASCADE,related_name="refund_items")
    fund_accounts = models.ForeignKey(FundAccout,on_delete = models.CASCADE,related_name="refund_items")
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name="refund_items",null=True,blank=True)
    make_refund = models.CharField(max_length=64,verbose_name=("make refund for cash on delivery"),null = True,blank = True)


    class Meta:
        verbose_name_plural = "Request Refund Items"
    def __str__(self):
        return f"{self.order_item.id} - {self.fund_accounts.id}"
    
    def make_refund(self, **kwargs):
        if self.order_item.status in ["Request Refund"] and self.order_item.order.payment_mode in ["cod"]:
            url = reverse("payout")
            return format_html("<a href='%s'>%s</a>" % (url, "Refund"))

class Payout(TimeStampModel):

    # OrderItem F.K
    order_item = models.ForeignKey(OrderItem,related_name="payout",on_delete = models.CASCADE,null = True,blank = True) 
    # Order F.K 
    order = models.ForeignKey(Order, related_name="payout", on_delete = models.CASCADE,null = True,blank = True)

    razorpay_payout_id = models.CharField(max_length=64)
    fund_account_id = models.CharField(max_length=64)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3)
    fees  = models.CharField(max_length=64)
    tax = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    purpose = models.CharField(max_length=64)
    mode = models.CharField(max_length=64)
    reference_id = models.CharField(max_length=64)
    merchant_id = models.CharField(max_length=64)
    utr = models.CharField(max_length=64,null = True,blank=True)
    # errors
    source = models.CharField(max_length=64,null = True,blank=True)
    reason = models.CharField(max_length=64,null=True,blank=True)
    description = models.TextField(max_length = 255,null = True,blank=True)
    
    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Payouts"

