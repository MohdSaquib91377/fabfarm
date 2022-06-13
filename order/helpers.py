
from django.http import Http404

def get_order_object(razorpay_order_id):
    try:
        return Order.objects.get(razorpay_order_id = razorpay_order_id)
    except Order.DoesNotExist:
        raise Http404
    