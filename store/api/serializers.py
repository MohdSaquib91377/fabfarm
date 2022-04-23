from rest_framework import serializers

from store.models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image 
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class ProductsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_images")
    
    class Meta:
        model = Product
        fields = "__all__"


    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images,many=True)
        return serializer.data



class ProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"