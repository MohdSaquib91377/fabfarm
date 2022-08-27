
from django.http import Http404
from .models import *
from django.db.models import Q
import re
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