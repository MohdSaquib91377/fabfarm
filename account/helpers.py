from rest_framework_simplejwt.tokens import RefreshToken
from account.models import *

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
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

    