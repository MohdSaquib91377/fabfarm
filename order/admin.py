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
    list_display = ["order","product","id","price","quantity","status","make_refund"]

  

