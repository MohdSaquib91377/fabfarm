import razorpay
from django.conf import settings
import hashlib
import hmac
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

    # response["razorpay_order_id"] = ordered.razorpay_order_id
    # response["amount"] = order_amount
    

    return ordered.razorpay_order_id



    
# Verify Payment Signature🔗

def verify_signature(data:dict,key=settings.RAZOR_KEY_SECRET):
    message = f"{data.get('razorpay_order_id', '')}|{data.get('razorpay_payment_id','')}"
    return hmac.new(
        key.encode(), message.encode(), hashlib.sha256
    ).hexdigest() == data.get("razorpay_signature", "")
