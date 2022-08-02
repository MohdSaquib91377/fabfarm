from django.contrib import admin
from .models import Payment,Refund
# Register your models here.

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = [
                    'id', 'razorpay_refund_id', 'razorpay_payment_id','order', 'payment','user','amount',
                    'speed','status','speed_requested','speed_processed'
                    ]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id","order","user","razorpay_payment_id",
                    "razorpay_order_id","razorpay_signature",
                    "method","fee","tax","error_code","error_description",
                    "error_source","error_step","error_reason","error_order_id",
                    "error_payment_id"
                    ]