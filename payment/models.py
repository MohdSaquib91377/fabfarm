from distutils.log import error
from statistics import mode
from account.models import TimeStampModel,CustomUser
from order.models import Order,OrderItem
from django.db import models
from account.models import CustomUser

class Payment(TimeStampModel):
    order = models.ForeignKey(Order, related_name="payment",on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="payment",on_delete = models.CASCADE)

    # payment successful
    razorpay_payment_id = models.CharField(max_length=64,null=True,blank=True)
    razorpay_order_id = models.CharField(max_length=64,null=True,blank=True)
    razorpay_signature = models.CharField(max_length= 64,null=True,blank=True)
    method = models.CharField(max_length=64,null=True,blank=True)
    fee = models.CharField(max_length=64,null=True,blank=True)
    tax = models.CharField(max_length=64,null=True,blank=True)

    # payment Errors
    error_code = models.TextField(null=True,blank=True)
    error_description = models.TextField(null=True,blank=True)
    error_source = models.TextField(null=True,blank=True)
    error_step = models.TextField(null=True,blank=True)
    error_reason = models.CharField(max_length = 64,null=True,blank=True)
    error_order_id = models.TextField(null=True,blank=True)
    error_payment_id = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'Payments'


class Refund(TimeStampModel):
    razorpay_refund_id = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="refunds",null=True, blank=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE,null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,related_name="refunds",null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="refunds",null=True, blank=True)
    amount = models.FloatField()
    speed = models.CharField(max_length=50, null=True, blank=True)
    # speed
    #   options :- normal(refund will take 5-7 working days.)
    #   optimum :- indicates that the refund will be processed at an optimal speed based on Razorpay's internal fund transfer logic
    status = models.CharField(max_length=50, null=True, blank=True)
    # status
    # pending :- This state indicates that Razorpay is attempting to process the refund.
    # processed :- this is the final state of the refund.
    # failed :-  A refund can attain the failed state in the following scenarios
    #         Normal refund not possible for a payment which is more than 6 months old.
    #         Instant Refund can sometimes fail because of customer's account or bank-related issues.
    speed_requested = models.CharField(max_length=64,null=True,blank=True)
    # normal
    # optimum
    speed_processed = models.CharField(max_length=50, blank=True, null=True)
    # instant: This means that the refund has been processed instantly via fund transfer.
    # normal: This means that the refund has been processed by the payment processing partner. That is, the refund will take 5-7 working days.

    class Meta:
        db_table = "refunds"

