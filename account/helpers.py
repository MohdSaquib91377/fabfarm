import email
from genericpath import exists
from imp import cache_from_source
from os import stat
import re
from sys import prefix
from types import new_class
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import *
from services.email import *
from services.otp import *
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.contrib.auth.hashers import make_password

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
   

def clear_cache(keys):
    cache.delete(keys)

# generate random otp 
def generate_otp(data):
    otp_list = []
    for k,v in data.items():
        otp = get_random_string(length=6,allowed_chars="0123456789")
        otp_list.append(otp)
    # store data in cache
    txn_id = get_random_string(length=6,allowed_chars="0123456789")
    expire_at = timezone.now()+settings.OTP['OTP_EXPIRATION_TIME']
    data = {
        "txn_id":txn_id,
        "new_otp":otp_list[0],
        "new_email":data["new_otp"],
        "exists_otp":otp_list[1],
        "exists_email":data["exists_otp"],
        "expire_at":expire_at
    }
    cache.set(f"{txn_id}", data, timeout=CACHE_TTL)
    return cache.get(f"{txn_id}")
    
# Alway send otp verify otp should be reusable
def verify_otp(data):
    error_list = []
    msg = "OTP verification successful"
    status = 200
    is_otp_found = CustomUser.objects.filter(id = data['txn_id'] ,otp = data['otp']).first()
    if is_otp_found:
        if not is_otp_found.is_expired:
            CustomUser.objects.filter(id = data['txn_id'],otp = data['otp']).update(is_verified=True)
            return msg,status
        msg = {"otp" : "OTP expired","status" : 400}
        return msg,status

    msg = {"otp" : "Invalid OTP ", "status" : 400}
    status = 404
    return msg,status


def send_otp_on_entered_email_or_exists_one(data):
    msg = ""
    status = 200
    user = CustomUser.objects.filter(id = data.get('user_id'),email_or_mobile = data.get('new_email')).first()
    if user:
        msg = {"email_or_mobile":"already verify"}
        status = 400
        return msg,status

    elif CustomUser.objects.filter(email_or_mobile=data.get('new_email')).exists():
        msg = {"email_or_mobile":"is taken by someone"}
        status = 400
        return msg,status

    else:
        # send email
        response = generate_otp({"new_otp":data.get('new_email'),"exists_otp":data.get('exists_email')})
        send_mail(f"we have send you OTP on this {data.get('new_email')} please verify",f"your OTP is {response.get('new_otp')}",[data.get('new_email'),data.get('new_email')])

        send_mail(f"we have send you OTP on this {data.get('exists_email')} please verify",f"your OTP is {response.get('exists_otp')}",[data.get('exists_email'),data.get('exists_email')])

        msg = {
            "new_email_otp":f"OTP sent on {data.get('new_email')}",
            "exists_email_otp":f"OTP sent on {data.get('exists_email')}",
            "txn_id":f"{response.get('txn_id')}",
            
            }
        status = 200
        return msg,status


def verify_updated_email_or_exists_one(data):
    status = 200
    msg = "Email updated successfully"
    # read data from cache
    response = cache.get(data.get('txn_id'))

    if not response:
        status = 400
        msg = {"new_email_otp":"Invalid OTP"} 
        return msg,status

    elif response.get('new_otp') != data.get('new_email_otp'):
        status = 400
        msg = {"new_email_otp":"Invalid OTP"} 
        return msg,status
    
    elif response.get('exists_otp') != data.get('exists_email_otp'):
        status = 400
        msg = {"exists_email_otp":"Invalid OTP"} 
        return msg,status
    

    elif timezone.now() > response.get('expire_at'):
        status = 400
        msg = {"new_email_otp":"otp expired","exists_email_otp":"otp expired"} 
        return msg,status


    elif CustomUser.objects.filter(email_or_mobile=response.get('exists_email')).first().check_password(data.get('password')):
        CustomUser.objects.filter(email_or_mobile=response.get('exists_email')).update(email_or_mobile=response.get('new_email'))
        clear_cache(f"{data.get('txn_id')}")
        return msg,status

    else:
        status = 400
        msg = {"password":"Invalid password"} 
        return msg,status

        
# generate random otp 
def generate_otp_for_mobile(data):
    otp_list = []
    for k,v in data.items():
        otp = get_random_string(length=6,allowed_chars="0123456789")
        otp_list.append(otp)
    # store data in cache
    txn_id = get_random_string(length=6,allowed_chars="0123456789")
    expire_at = timezone.now()+settings.OTP['OTP_EXPIRATION_TIME']
    data = {
        "txn_id":txn_id,
        "new_otp":otp_list[0],
        "new_mobile":data["new_otp"],
        "exists_otp":otp_list[1],
        "exists_email_or_mobile":data["exists_otp"],
        "expire_at":expire_at
    }
    cache.set(f"{txn_id}", data, timeout=CACHE_TTL)
    return cache.get(f"{txn_id}")
    





def send_otp_on_entered_mobile_or_exists_one(data):
    status = 200
    msg = ""
    if CustomUser.objects.filter(id = data.get('user_id'),mobile = data.get('new_mobile'),is_mobile_verified=True).exists():
        status = 400
        msg = {"mobile":"Mobile Already verified"}
        return msg,status

    elif CustomUser.objects.filter(mobile = data.get('new_mobile')).exists():
        status = 400
        msg = {"mobile":f"{data.get('new_mobile')} taken by someone"}
        return msg,status

    
    if data.get('exists_mobile') is None:
        user = CustomUser.objects.filter(id = data.get('user_id')).first()
        response = generate_otp_for_mobile({"new_otp":data.get('new_mobile'),"exists_otp":user.email_or_mobile})
        send_twilio_sms(f"{response['new_mobile']}",f"this is your otp {response['new_otp']} please verify")
        send_mail(f"we have send you otp on this {user.email_or_mobile} please verify",f"your otp is {response['exists_otp']}",[user.email_or_mobile])
        
        msg = {
                "new_mobile_otp":f"OTP sent on {response['new_mobile']}",
                "exists_email_or_mobile_otp":f"OTP sent on {response['exists_email_or_mobile']}",
                "txn_id":f"{response.get('txn_id')}",
            }
        return msg,status

    else:
        response = generate_otp_for_mobile({"new_otp":data.get('new_mobile'),"exists_otp":data.get('exists_mobile')})
        send_twilio_sms(f"{response['new_mobile']}",f"this is your otp {response['new_otp']} please verify")
        send_twilio_sms(f"{response['exists_email_or_mobile']}",f"this is your otp {response['exists_otp']} please verify")

        msg = {
            "new_mobile_otp":f"OTP sent to {response['new_mobile']}",
            "exists_email_or_mobile_otp":f"OTP sent to {response['exists_email_or_mobile']}",
            "txn_id":f"{response['txn_id']}",
            }
        return msg,status


def verify_and_update_mobile(data,user):
    response = cache.get(data.get('txn_id'))
    if not response:
        status = 400
        msg = {"new_mobile_otp":"Invalid OTP"}  
        return msg,status


    elif response.get('new_otp') != (data.get('new_mobile_otp')):
        status = 400
        msg = {"new_mobile_otp":"Invalid OTP"}  
        return msg,status

    elif response["exists_otp"] != data.get('exists_email_or_mobile_otp'):
        status = 400
        msg = {"exists_email_or_mobile_otp":"Invalid OTP"}  
        return msg,status


    elif timezone.now() > response.get('expire_at'):
        status = 400
        msg = {"new_mobile_otp":"OTP expired"}  
        return msg,status


    elif CustomUser.objects.filter(id = user.id).first().check_password(data.get('password')):
        CustomUser.objects.filter(id = user.id).update(mobile = response["new_mobile"],is_mobile_verified=True)
        clear_cache(f"{data.get('txn_id')}")
        status = 200
        msg = f"Mobile updated SuccessFully"
    
        return msg,status
    else:
        status = 400
        msg = {"password":"Invalid password"} 
        return msg,status
        
def get_user_info(user):
    user_info = {
    "fullname": user.fullname,
    "email_or_mobile": user.email_or_mobile
    }

    return user_info