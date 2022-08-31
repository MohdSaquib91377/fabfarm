
from django.http import Http404
from .models import *
from django.db.models import Q
import re
from django.db.models import Sum

def get_order_object(razorpay_order_id):
    try:
        return Order.objects.get(razorpay_order_id = razorpay_order_id)
    except Order.DoesNotExist:
        raise Http404
    
def update_order_status(order_id):
    total_number_of_items = OrderItem.objects.filter(order_id = order_id)
    number_of_items_cancel = OrderItem.objects.filter(order_id = order_id,status = "Cancelled")
    if total_number_of_items.count() > 0 and number_of_items_cancel.count() > 0:
        if total_number_of_items.count() == number_of_items_cancel.count():
            Order.objects.filter(id = order_id).update(order_status = "order cancelled")
            return True
        else:
            return False

def is_ValidIFSCode(ifsc_code): 
    # Regex to check valid IFSC Code.
    regex = "^[A-Z]{4}0[A-Z0-9]{6}$"

    # Compile the ReGex
    p = re.compile(regex)

    if(re.search(p, ifsc_code)):
        return True
    else:
        return False



def update_payout(data):
    payout = Payout.objects.filter(razorpay_payout_id = data["id"]).first()
    if not payout:
        return ""
    payout.razorpay_payout_id = data["id"]
    payout.fund_account_id = data["fund_account_id"]
    payout.amount = int(data["amount"]/100)
    payout.currency = data["currency"]
    payout.fees = data["fees"]
    payout.tax = data["tax"]
    payout.status = data["status"]
    payout.purpose = data["purpose"]
    payout.utr = data["utr"]
    payout.mode = data["mode"]
    payout.reference_id = data["reference_id"]
    payout.save()

    if data["status"] == "reversed":
        payout.order.order_status = "partial refund failed"
        payout.source = data['error']["source"]
        payout.reason = data['error']["reason"]
        payout.description = data['error']["description"]

   

    elif data["status"] == "processed":
        # TODO: Shoot a mail to customer
        payout_order_total = Payout.objects.filter(order__id = payout.order.id,status = "processed").aggregate(Sum('amount'))['amount__sum']

        if payout.order.total_price - payout_order_total > 0:
            payout.order.order_status = "partial order"
            payout.order.payment_status = "Payment Refund Partial"
            payout.order_item.status = "Refunded"
        else:
            payout.order.order_status = "order cancelled"
            payout.order.payment_status = "Payment Refund Full"
            payout.order_item.status = "Refunded"   
        
    payout.order_item.save()
    payout.order.save()








from django.conf import settings
import json
import requests,base64


raz_cred = f"{settings.RAZOR_KEY_ID}:{settings.RAZOR_KEY_SECRET}"
raz_token = base64.b64encode(raz_cred.encode()).decode()
RAZORPAY_BASE_URL = "https://api.razorpay.com/v1/"

def create_contact(url: str,data:dict) -> dict:
    response = requests.post(
        url = RAZORPAY_BASE_URL + url,
        headers = {"Authorization": f"Basic {raz_token}","Content-Type": "application/json",},
        data = json.dumps(data)
        )   
    return response.json(),response.status_code

def create_fund_account(url: str,data:dict) -> dict:
    response = requests.post(
        url = RAZORPAY_BASE_URL + url,
        headers = {"Authorization": f"Basic {raz_token}","Content-Type": "application/json",},
        data = json.dumps(data)
        )
    return response.json(),response.status_code

def create_payout(url: str,data:dict) -> dict:
    response = requests.post(
        url = RAZORPAY_BASE_URL + url,
        headers = {"Authorization": f"Basic {raz_token}","Content-Type": "application/json",},
        data = json.dumps(data)

        ) 
    return response.json(),response.status_code