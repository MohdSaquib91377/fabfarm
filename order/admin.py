from django.contrib import admin
from order.models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","full_name","city","state","country",
                    "pincode","locality","landmark","address",
                    "alternate_number","total_price","payment_mode",
                    "payment_id","message","tracking_no","coupon",
                    "discounted_price","total_amount_payble","razorpay_order_id",
                    "razorpay_status","amount_due","amount_paid","attempts",
    ]
admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order","product","price","quantity","status"]

admin.site.register(OrderItem,OrderItemAdmin)