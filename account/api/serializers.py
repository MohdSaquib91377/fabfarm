from rest_framework import serializers
from account.models  import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fullname','email_or_mobile','password']