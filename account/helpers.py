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

# generate random otp 
def generate_otp(key,email):
    otp = get_random_string(length=6,allowed_chars="0123456789")
    expire_at = timezone.now()+settings.OTP['OTP_EXPIRATION_TIME']
    data = {
        "otp": otp,
        "expire_at": expire_at,
        "email":email
    }
    # store data in cache
    cache.set(f"{key}", data, timeout=CACHE_TTL)
    return cache.get(f"{key}")
    
# Alway send otp verify otp should be reusable
def verify_otp(data):
    msg = "otp verification successful"
    status = 200
    is_otp_found = CustomUser.objects.filter(id = data['txn_id'] ,otp = data['otp']).first()
    if is_otp_found:
        if not is_otp_found.is_expired:
            CustomUser.objects.filter(id = data['txn_id'],otp = data['otp']).update(is_verified=True)
            return msg,status

        msg = "otp expired"
        status = 400
        return msg,status

    msg = "otp not found"
    status = 404
    return msg,status


def send_otp_on_entered_email_or_exists_one(data):
    msg = ""
    status = 200
    user = CustomUser.objects.filter(id = data.get('user_id'),email_or_mobile = data.get('new_email')).first()
    if user:
        msg = f"user {data.get('new_email')} already verify"
        status = 400
        return msg,status

    elif CustomUser.objects.filter(email_or_mobile=data.get('new_email')).exists():
        msg = f"this {data.get('new_email')} is taken by someone"
        status = 400
        return msg,status

    else:
        # send email
        cache_response = generate_otp("new_email",f"{data.get('new_email')}")
        send_mail(f"we have send you otp on this {data.get('new_email')} please verify",f"your otp is {cache_response.get('otp')}",[data.get('new_email'),data.get('new_email')])

        cache_response = generate_otp("exists_email",f"{data.get('exists_email')}")
        send_mail(f"we have send you otp on this {data.get('exists_email')} please verify",f"your otp is {cache_response.get('otp')}",[data.get('exists_email'),data.get('exists_email')])

        msg = f"we have send you otp on this {data.get('new_email')} or {data.get('exists_email')} please verify"
        status = 200
        return msg,status


def verify_updated_email_or_exists_one(data):
    status = 200
    msg = "Email updated successfully"
    # read data from cache
    new_email_chache_response = cache.get("new_email")
    exists_email_chache_response = cache.get("exists_email")
    if new_email_chache_response.get('otp') != data.get('new_email_otp') or exists_email_chache_response.get('otp') != data.get('exists_email_otp'):
        status = 404
        msg = "invalid otp"
        return msg,status
        
    elif timezone.now() > new_email_chache_response.get('expire_at') or timezone.now() > exists_email_chache_response.get('expire_at'):
        status = 400
        msg = "otp expired"
        return msg,status

    else:
        password = make_password(data.get('password'))
        CustomUser.objects.filter(email_or_mobile=exists_email_chache_response.get('email')).update(email_or_mobile=new_email_chache_response.get('email'),password=password)
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

def clear_cache(keys):
    for key in keys:
        cache.delete(key)

def send_otp_on_entered_mobile_or_exists_one(data):
    status = 200
    msg = ""
    if CustomUser.objects.filter(id = data.get('user_id'),mobile = data.get('new_mobile'),is_mobile_verified=True).exists():
        status = 400
        msg = f"{data.get('new_mobile')} already verify"
        return msg,status

    elif CustomUser.objects.filter(mobile = data.get('new_mobile')).exists():
        status = 401
        msg = f"{data.get('new_mobile')} taken by someone"
        return msg,status

    # generate otp 
    new_mobile_cache_response = generate_otp_for_mobile(f"{data.get('new_mobile')}")

    # send sms
    send_twilio_sms(f"{data.get('new_mobile')}",f"this is your otp {new_mobile_cache_response.get('otp')} please verify")
    if data.get('exists_mobile') is None:
        user = CustomUser.objects.filter(id = data.get('user_id')).first()
        email_or_mobile_cache_response = generate_otp_for_mobile(f"{user.email_or_mobile}")
        send_mail(f"we have send you otp on this {user.email_or_mobile} please verify",f"your otp is {email_or_mobile_cache_response.get('otp')}",[user.email_or_mobile])
        msg = f"we have send you an otp on your {data.get('new_mobile')} or {user.email_or_mobile}"
        return msg,status

    else:
        email_or_mobile_cache_response = generate_otp_for_mobile(f"{data.get('exists_mobile')}")   
        send_twilio_sms(f"{data.get('exists_mobile')}",f"this is your otp {email_or_mobile_cache_response.get('otp')} please verify")
        msg = f"we have send you an otp on your {data.get('new_mobile')} or {data.get('exists_mobile')}"
        return msg,status
        
def verify_and_update_mobile(data,user):
    new_mobile_cache_response = cache.get(data.get('new_mobile_otp'))
    email_or_mobile_cache_response = cache.get(data.get('exists_email_or_mobile_otp'))

    if not new_mobile_cache_response or not email_or_mobile_cache_response:
        status = 400
        msg = f"invalid otp"   
        return msg,status
    elif new_mobile_cache_response.get('otp') != data.get('new_mobile_otp') or email_or_mobile_cache_response.get('otp') != data.get('exists_email_or_mobile_otp'):
        status = 400
        msg = f"invalid otp"   
        return msg,status

    elif timezone.now() > new_mobile_cache_response.get('expire_at') or timezone.now() > email_or_mobile_cache_response.get('expire_at'):
        status = 400
        msg = f"otp expired"   
        return msg,status

    CustomUser.objects.filter(id = user.id).update(mobile = new_mobile_cache_response.get('email_or_mobile'),is_mobile_verified=True)
    clear_cache({"name":data.get('new_mobile_otp'),"name":data.get('exists_email_or_mobile_otp')})
    status = 200
    msg = f"Mobile updated SuccessFully"
  
    return msg,status
