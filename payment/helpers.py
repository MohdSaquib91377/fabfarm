from weakref import ref
from xmlrpc import client
from payment.models import Payment
import razorpay
from django.conf import settings
import hashlib
import hmac
from order.models import *
from payment.models import *
from store.models import *
from django.db.models import Sum


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
    payment = Payment.objects.filter(order_id=order_id).first()
    return payment.razorpay_payment_id


# Create Refund for OrderItem
def create_refund(order,order_item_price):
    client = get_razorpay_client()
    refund = client.payment.refund(get_payment_object_by_order_id(order.id),{
    "amount": int(order_item_price*100),
    "speed": "normal",
    })
    return refund

def update_order(payload):
    print("update order ---------------------------->>>>>>>>>")
    '''
                {
            "entity": "event",
            "account_id": "acc_Ja7clXrWRXJTJC",
            "event": "refund.processed",
            "contains": [
                "refund",
                "payment"
            ],
            "payload": {
                "refund": {
                "entity": {
                    "id": "rfnd_JwiKLVZkhBuf5R",
                    "entity": "refund",
                    "amount": 50000,
                    "currency": "INR",
                    "payment_id": "pay_JwiFztYKfUAIUq",
                    "notes": [],
                    "receipt": null,
                    "acquirer_data": {
                    "rrn": null
                    },
                    "created_at": 1658558877,
                    "batch_id": null,
                    "status": "processed",
                    "speed_processed": "normal",
                    "speed_requested": "normal"
                }
                },
                "payment": {
                "entity": {
                    "id": "pay_JwiFztYKfUAIUq",
                    "entity": "payment",
                    "amount": 150000,
                    "currency": "INR",
                    "status": "captured",
                    "order_id": "order_JwiFvS5FddS8sL",
                    "invoice_id": null,
                    "international": false,
                    "method": "upi",
                    "amount_refunded": 50000,
                    "refund_status": "partial",
                    "captured": true,
                    "description": "Test Transaction",
                    "card_id": null,
                    "bank": null,
                    "wallet": null,
                    "vpa": "success@razorpay",
                    "email": "gaurav.kumar@example.com",
                    "contact": "+919999999999",
                    "notes": {
                    "address": "Razorpay Corporate Office"
                    },
                    "fee": 3540,
                    "tax": 540,
                    "error_code": null,
                    "error_description": null,
                    "error_source": null,
                    "error_step": null,
                    "error_reason": null,
                    "acquirer_data": {
                    "rrn": "152939349384",
                    "upi_transaction_id": "5FFBE4C7233FEEA010BAFE5698B379E8"
                    },
                    "created_at": 1658558630
                }
                }
            },
            "created_at": 1658558877
            }	'''
    razorpay_refund = payload['refund']['entity']
    refund = Refund.objects.filter(razorpay_refund_id = razorpay_refund['id']).first()
    if refund:
        '''
                "id": "rfnd_JwiKLVZkhBuf5R",
                "entity": "refund",
                "amount": 50000,
                "currency": "INR",
                "payment_id": "pay_JwiFztYKfUAIUq",
                "notes": [],
                "receipt": null,
                "acquirer_data": {
                "rrn": null
                },
                "created_at": 1658558877,
                "batch_id": null,
                "status": "processed",
                "speed_processed": "normal",
                "speed_requested": "normal"
        '''
        # Refund failed
        if razorpay_refund["status"] == 'failed':
            refund.order.order_status = "partial refund failed"
            refund.save()
            return ""

       
       

        payment_id = payload["payment"]["entity"]["id"]
        total_refund_amount = Refund.objects.filter(razorpay_payment_id = payment_id).aggregate(Sum('amount'))["amount__sum"]

       

        refund.status = razorpay_refund['status']
        refund.speed_requested = razorpay_refund["speed_requested"]
        refund.speed_processed = razorpay_refund["speed_processed"]
        refund.amount = razorpay_refund["amount"] / 100

         # Refund Full
        if int(refund.order.total_price) - total_refund_amount<= 0:
            refund.order.order_status = "order cancelled"
            refund.order.payment_status = "Payment Refund Full"
            refund.order_item.status = "Refund"
            
        # Refund proccess
        else:
            refund.order.order_status = "partial order"
            refund.order.payment_status = "Payment Refund Partial"
            refund.order_item.status = "Refund"
            
        refund.save()
        refund.order.save()
        refund.order_item.save()
        # update product quantity
        order_item_quantity = refund.order_item.quantity
        product_id = refund.order_item.product.id
        product_obj = Product.objects.get(id = product_id)
        product_obj.quantity += int(order_item_quantity)
        product_obj.save(update_fields = ["quantity"])

        
        
        