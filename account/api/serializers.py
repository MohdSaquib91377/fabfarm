from pyexpat import model
from attr import fields
from rest_framework import serializers
from account.models  import CustomUser

class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=64)
    email_or_mobile = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

class OTPVerifySerializer(serializers.Serializer):
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

