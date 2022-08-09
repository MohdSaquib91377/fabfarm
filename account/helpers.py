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
    for key in keys:
        cache.delete(key)

# generate random otp 
def generate_otp(email):
    otp = get_random_string(length=6,allowed_chars="0123456789")
    expire_at = timezone.now()+settings.OTP['OTP_EXPIRATION_TIME']
    data = {
        "otp": otp,
        "expire_at": expire_at,
        "email":email
    }
    # store data in cache
    cache.set(f"{otp}", data, timeout=CACHE_TTL)
    return cache.get(f"{otp}")
    
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
        cache_response = generate_otp(f"{data.get('new_email')}")
        send_mail(f"we have send you OTP on this {data.get('new_email')} please verify",f"your OTP is {cache_response.get('otp')}",[data.get('new_email'),data.get('new_email')])

        cache_response = generate_otp(f"{data.get('exists_email')}")
        send_mail(f"we have send you OTP on this {data.get('exists_email')} please verify",f"your OTP is {cache_response.get('otp')}",[data.get('exists_email'),data.get('exists_email')])

        msg = {
            "new_email_otp":f"OTP sent on {data.get('new_email')}",
            "exists_email_otp":f"OTP sent on {data.get('exists_email')}"
            }
        status = 200
        return msg,status


def verify_updated_email_or_exists_one(data):
    status = 200
    msg = "Email updated successfully"
    # read data from cache
    new_email_chache_response = cache.get(data.get('new_email_otp'))
    exists_email_chache_response = cache.get(data.get('exists_email_otp'))

    if not new_email_chache_response:
        status = 400
        msg = {"new_email_otp":"Invalid OTP"} 
        return msg,status

    elif not exists_email_chache_response:
        status = 400
        msg = {"exists_email_otp":"Invalid OTP"}
        return msg,status

    elif new_email_chache_response.get('otp') != data.get('new_email_otp'):
        status = 400
        msg = {"new_email_otp":"Invalid OTP"} 
        return msg,status
    
    elif exists_email_chache_response.get('otp') != data.get('exists_email_otp'):
        status = 400
        msg = {"exists_email_otp":"Invalid OTP"} 
        return msg,status
    

    elif timezone.now() > new_email_chache_response.get('expire_at'):
        status = 400
        msg = {"new_email_otp":"otp expired"} 
        return msg,status

    elif timezone.now() > exists_email_chache_response.get('expire_at'):
        status = 400
        msg = {"exists_email_otp":"otp expired"} 
        return msg,status

    else:
        password = make_password(data.get('password'))
        CustomUser.objects.filter(email_or_mobile=exists_email_chache_response.get('email')).update(email_or_mobile=new_email_chache_response.get('email'),password=password)
        clear_cache({f"{data.get('new_email_otp')}":data.get('new_email_otp'),f"{data.get('exists_email_otp')}":data.get('exists_email_otp')})
        return msg,status

# generate random otp 
def generate_otp_for_mobile(email_or_mobile):
    otp = get_random_string(length=6,allowed_chars="0123456789")
    expire_at = timezone.now()+settings.OTP['OTP_EXPIRATION_TIME']
    data = {
        "otp": otp,
        "expire_at": expire_at,
        "email_or_mobile":email_or_mobile
    }
    # store data in cache
    cache.set(f"{otp}", data, timeout=CACHE_TTL)
    return cache.get(f"{otp}")



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

    # generate otp 
    new_mobile_cache_response = generate_otp_for_mobile(f"{data.get('new_mobile')}")

    # send sms
    send_twilio_sms(f"{data.get('new_mobile')}",f"this is your otp {new_mobile_cache_response.get('otp')} please verify")
    if data.get('exists_mobile') is None:
        user = CustomUser.objects.filter(id = data.get('user_id')).first()
        email_or_mobile_cache_response = generate_otp_for_mobile(f"{user.email_or_mobile}")
        send_mail(f"we have send you otp on this {user.email_or_mobile} please verify",f"your otp is {email_or_mobile_cache_response.get('otp')}",[user.email_or_mobile])
        msg = {
            "new_mobile_otp":f"OTP sent to {data.get('new_mobile')}",
            "exists_email_or_mobile_otp":f"OTP sent to {user.email_or_mobile}"
            }
        return msg,status

    else:
        email_or_mobile_cache_response = generate_otp_for_mobile(f"{data.get('exists_mobile')}")   
        send_twilio_sms(f"{data.get('exists_mobile')}",f"this is your otp {email_or_mobile_cache_response.get('otp')} please verify")
        msg = {
            "new_mobile_otp":f"OTP sent to {data.get('new_mobile')}",
            "exists_email_or_mobile_otp":f"OTP sent to {user.email_or_mobile}"
            }
        return msg,status


def verify_and_update_mobile(data,user):
    new_mobile_cache_response = cache.get(data.get('new_mobile_otp'))
    email_or_mobile_cache_response = cache.get(data.get('exists_email_or_mobile_otp'))

    if not new_mobile_cache_response:
        status = 400
        msg = {"new_mobile_otp":"Invalid OTP"}  
        return msg,status

    elif not email_or_mobile_cache_response:
        status = 400
        msg = {"exists_email_or_mobile_otp":"Invalid OTP"}  
        return msg,status

    elif new_mobile_cache_response.get('otp') != data.get('new_mobile_otp'):
        status = 400
        msg = {"new_mobile_otp":"Invalid OTP"}  
        return msg,status

    elif email_or_mobile_cache_response.get('otp') != data.get('exists_email_or_mobile_otp'):
        status = 400
        msg = {"exists_email_or_mobile_otp":"Invalid OTP"}  
        return msg,status


    elif timezone.now() > new_mobile_cache_response.get('expire_at'):
        status = 400
        msg = {"new_mobile_otp":"OTP expired"}  
        return msg,status

    elif timezone.now() > email_or_mobile_cache_response.get('expire_at'):
        status = 400
        msg = {"exists_email_or_mobile_otp":"OTP expired"}  
        return msg,status

    CustomUser.objects.filter(id = user.id).update(mobile = new_mobile_cache_response.get('email_or_mobile'),is_mobile_verified=True)
    clear_cache({f"{data.get('new_mobile_otp')}":data.get('new_mobile_otp'),f"{data.get('exists_email_or_mobile_otp')}":data.get('exists_email_or_mobile_otp')})
    status = 200
    msg = f"Mobile updated SuccessFully"
  
    return msg,status

def get_user_info(user):
    user_info = {
    "fullname": user.fullname,
    "email_or_mobile": user.email_or_mobile
    }

    return user_info