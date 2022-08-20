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


def validate_cod_refund(order_item):
    order_item_obj = OrderItem.objects.filter(id = order_item.id,status = "Request Refund").first()
    if order_item_obj:
        if not order_item_obj.is_return:
            raise ValidationError(f"Refund Cannot be proccessed until product not return")
    return order_item


class RequestRefundBankInfo(TimeStampModel):
    ifsc_code = models.CharField(max_length = 64)
    account_number = models.PositiveBigIntegerField()
    confirm_account_number = models.PositiveBigIntegerField()
    account_holder_name = models.CharField(max_length = 64)
    phone_number = models.PositiveBigIntegerField()
    reason = models.CharField(max_length = 256,null = True, blank = True)
    #order item
    order_item = models.ForeignKey(OrderItem,on_delete = models.CASCADE,related_name = "RequestRefundBankInfo",null = True,blank = True,validators=[validate_cod_refund])
    order = models.ForeignKey(Order,on_delete = models.CASCADE,related_name = "RequestRefundBankInfo",null = True,blank = True)
    price = models.PositiveBigIntegerField(default = 0)
    is_refunded = models.BooleanField(default = False)
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "RequestRefundBankInfo",null = True,blank = True)

    def __str__(self):
        return f"{self.account_number}"



      
            

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
def create_receive_return(sender,instance,*args,**kwargs):
    if instance.is_return == True:
        obj, created = ReceiveReturn.objects.get_or_create(
            order_item=instance,
            order=instance.order,
            product=instance.product
        )

    else:
        if ReceiveReturn.objects.filter(order_item = instance).exists():
            ReceiveReturn.objects.filter(order_item = instance).delete()

            
@receiver(post_save,sender = RequestRefundBankInfo)
def update_order_order_item_status_or_product_quantity(sender,instance,*args,**kwargs):
    if instance.is_refunded == True:
        total_order_item = RequestRefundBankInfo.objects.filter(order = instance.order).aggregate(Sum('price'))["price__sum"]
        if int(instance.order_item.order.total_amount_payble )- int(total_order_item) > 0:
            instance.order_item.order.order_status = "partial order"
            instance.order_item.order.payment_status = "Payment Refund Partial"
            instance.order_item.status = "Refunded"
        else:
            instance.order_item.order.order_status  = "order cancelled"
            instance.order_item.order.payment_status = "Payment Refund Full"
            instance.order_item.status = "Refunded"
        instance.order_item.save()
        instance.order_item.order.save()
        # update product quantity
        product = Product.objects.filter(id = instance.order_item.product.id).first()
        product.quantity += instance.order_item.quantity
        product.save()