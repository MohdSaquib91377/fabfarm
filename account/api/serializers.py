from pyexpat import model
from rest_framework import serializers
from account.models  import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

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

