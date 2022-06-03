import razorpay
from django.conf import settings
client = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
def create_order(data,ordered):
    payment = client.order.create(data)
    ordered.razorpay_order_id = payment['id']
    ordered.status = payment['status']
    ordered.amount_paid = payment['amount_paid']
    ordered.amount_due = payment['amount_due']
    ordered.attempts = payment['attempts']
    ordered.save()

    return Response({
        "razorpay_order_id":ordered.razorpay_order_id,
        "amount":ordered.total_amount_payble
    })