import razorpay
from django.conf import settings
client = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
def create_razorpay_order(ordered):
    response = dict()
    order_amount = int(ordered.total_amount_payble*100) 
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    payment = client.order.create({
        "amount": order_amount,
        "currency":order_currency,
        "receipt": order_currency
    })
    ordered.razorpay_order_id = payment['id']
    ordered.amount_paid = payment['amount_paid']
    ordered.amount_due = payment['amount_due']
    ordered.attempts = payment['attempts']
    ordered.razorpay_status = payment['status']
    ordered.save()

    response["razorpay_order_id"] = ordered.razorpay_order_id
    response["amount"] = order_amount
    response["status"] = "200"
    response["message"] = "Your ordered has been placed successfully successfuly"
    return response