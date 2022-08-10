from asyncio.format_helpers import extract_stack
from dataclasses import field, fields
import email
from pyexpat import model
from re import M
from ssl import VerifyFlags
from statistics import mode
from rest_framework import serializers
from account.models  import CustomUser, UserAddress
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=64)
    email_or_mobile = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

class OTPVerifySerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField(max_length=64)
    id = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=8)


class SendOTPSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField(max_length=64)

class LoginSerializer(serializers.ModelSerializer):
    email_or_mobile = serializers.CharField(max_length=64)
    class Meta:
        model = CustomUser
        fields = ['email_or_mobile','password']
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token":("Token is expired or invalid")
    }

    def validate(self,attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=64)
    new_password = serializers.CharField(max_length=64)
    confirm_password = serializers.CharField(max_length=64)
    otp = serializers.CharField(max_length=64)
    txn_id = serializers.CharField(max_length=64)

class ListUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["fullname","gender","email_or_mobile","mobile"]
        extra_fields = {"email_or_mobile":{"required": False, "allow_null": True},"mobile":{"required":False,"allow_null": True}}



class UpdateEmailSerializer(serializers.ModelSerializer):
    new_email_otp = serializers.CharField()
    exists_email_otp = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ["new_email_otp","exists_email_otp","password"]

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["mobile"]

class UpdateMobileSerializer(serializers.ModelSerializer):
    new_mobile_otp = serializers.CharField(max_length=64)
    exists_email_or_mobile_otp = serializers.CharField(max_length=64)

    class Meta:
        model = CustomUser
        fields = ["new_mobile_otp", "exists_email_or_mobile_otp", "password"]
        
class ForgotPasswordSerializer(serializers.Serializer):
    txn_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=64)
    set_password = serializers.CharField(max_length=64)



# UserAddress Serializer

class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = UserAddress
        fields = "__all__"
