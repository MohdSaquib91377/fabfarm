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


@admin.register(ReturnRefundPolicy)
class ReturnRefundPolicyAdmin(admin.ModelAdmin):
    list_display = ["id","return_refund_timestamp"]

@admin.register(ReceiveReturn)
class ReceiveReturnAdmin(admin.ModelAdmin):
    list_display = ["id","order","order_item","product"]

@admin.register(RequestRefundItem)
class RequestRefundItemAdmin(admin.ModelAdmin):
    list_display = ["id","order_item","fund_accounts","user","make_refund"]

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = [
     "razorpay_payout_id",
     "fund_account_id",
     "amount",
     "currency",
     "fees",
     "tax",
     "status",
     "purpose",
     "mode",
     "reference_id",
     "merchant_id",
     "source",
     "reason",
     "description"
    ]
    