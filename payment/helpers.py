from weakref import ref
from xmlrpc import client
from payment.models import Payment
import razorpay
from django.conf import settings
import hashlib
import hmac


def get_razorpay_client():
    client = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    return client

def create_razorpay_order(ordered):
    response = dict()
    order_amount = int(ordered.total_amount_payble*100) 
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    payment = get_razorpay_client().order.create({
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
    return ordered.razorpay_order_id,order_amount,settings.RAZOR_KEY_ID



    
# Verify razorpay Signature🔗

def verify_razorpay_signature(data:dict,key=settings.RAZOR_KEY_SECRET):
    message = f"{data.get('razorpay_order_id', '')}|{data.get('razorpay_payment_id','')}"
    return hmac.new(
        key.encode(), message.encode(), hashlib.sha256
    ).hexdigest() == data.get("razorpay_signature", "")

# verify payment signature
def payment_signature_varification(data:dict):
    return get_razorpay_client().utility.verify_payment_signature(data)

# Fetch An Order with id from razorpay server
def fetch_order_from_razor_pay(order_id):
    razorpay_order = get_razorpay_client().order.fetch(order_id)
    return razorpay_order

def get_payment_object_by_order_id(order_id):
    payment = Payment.objects.filter(id=order_id).first()
    return payment.razorpay_payment_id


# Create Refund for OrderItem
def create_refund(order,order_item_price):
    client = get_razorpay_client()
    refund = client.payment.refund(get_payment_object_by_order_id(order.id),{
    "amount": int(order_item_price*100),
    "speed": "normal",
    "notes": {
        "notes_key_1": "Refund for orderitem",
    },
    "receipt": f"{order.id}"
    })
    return refund

