from banner.models import *
from rest_framework import serializers
# Banner Serializer


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"



class PageSerializer(serializers.ModelSerializer):
    baners = BannerSerializer(many = True)
    class Meta:
        model = Page
        fields = "__all__"
