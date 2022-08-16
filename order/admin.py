from django.contrib import admin
from order.models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id","user","total_price","payment_mode",
                    "payment_id","tracking_no","coupon",
                    "discounted_price","total_amount_payble","razorpay_order_id",
                    "razorpay_status","amount_due","amount_paid","attempts", "created_at"
    ]
admin.site.register(Order,OrderAdmin)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order","product","id","price","quantity","status","make_refund","is_return"]

@admin.register(RequestRefundBankInfo)
class RequestRefundBankInfoAdmin(admin.ModelAdmin):
    list_display = ["id","created_at","updated_at","ifsc_code","account_number","confirm_account_number","account_holder_name","phone_number","order_item","is_refunded","price"]

@admin.register(ReturnRefundPolicy)
class ReturnRefundPolicyAdmin(admin.ModelAdmin):
    list_display = ["id","return_refund_timestamp"]

@admin.register(ReceiveReturn)
class ReceiveReturnAdmin(admin.ModelAdmin):
    list_display = ["id","order","order_item","product"]