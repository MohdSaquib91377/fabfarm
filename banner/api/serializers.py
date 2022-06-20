from banner.models import *
from rest_framework import serializers
# Banner Serializer
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
