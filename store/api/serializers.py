from pyexpat import model
from unicodedata import category
from attr import fields
from rest_framework import serializers

from store.models import *
from account.api.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image 
        fields = "__all__"



class ProductsSerializer(serializers.ModelSerializer):
    sub_category_name = serializers.CharField(source="sub_category.name")
    image = serializers.SerializerMethodField("get_images")
    brand = serializers.CharField(source="brand.name", read_only=True)
    maxQuantity = serializers.IntegerField(source = "quantity")
    quantity = serializers.SerializerMethodField("set_qauntity_by_1")
    class Meta:
        model = Product
        fields = ["id","name","slug","sku","price","old_price","is_active","is_bestseller","maxQuantity","quantity","description","meta_keywords","meta_description","brand","image","sub_category_name"]
        
    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images,many=True)
        return serializer.data

    def set_qauntity_by_1(self,obj):
        return 1

    

class SubCategoryProductSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name','products']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["id","name","sub_categories"]


class RecentViewProductSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    class Meta:
        model = RecentView
        fields ="__all__"