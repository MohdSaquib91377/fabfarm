from django.contrib import admin
from .models import Payment,Refund
# Register your models here.
admin.site.register(Payment)
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = [
                    'id', 'razorpay_refund_id', 'order', 'Payment','user','amount',
                    'speed','status','speed_requested','speed_processed'
                    ]