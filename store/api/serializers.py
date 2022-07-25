from __future__ import with_statement
from ast import Sub
from itertools import product
import re
from rest_framework import serializers
from wishlist.models import *
from store.models import *
from account.api.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image 
        fields = ["id","image_caption","image"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["id","name","sub_categories"]

class ProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    image = serializers.SerializerMethodField("get_images")
    brand = serializers.CharField(source="brand.name", read_only=True)
    maxQuantity = serializers.IntegerField(source = "quantity")
    quantity = serializers.SerializerMethodField("set_qauntity_by_1")
    is_product_in_wishlist_for_current_user = serializers.SerializerMethodField("get_cuurent_user_wishlist")

    class Meta:
        model = Product
        fields = ["id","name","slug","sku","price","old_price","is_active","is_bestseller","maxQuantity","quantity","description","meta_keywords","meta_description","brand","image","sub_category","category","is_product_in_wishlist_for_current_user"]
        
    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images,many=True)
        return serializer.data

    def set_qauntity_by_1(self,obj):
        return 1

    def get_cuurent_user_wishlist(self, obj):
        user = self.context.get('user')
        if user is not None:
            if Wishlist.objects.filter(product_id=obj.id, user=user).exists():
                return True
            else:
                return False
        
        
class SubCategoryProductSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)
    is_product_in_wishlist_for_current_user = serializers.SerializerMethodField("get_cuurent_user_wishlist")
    class Meta:
        model = SubCategory
        fields = ["id", "name", "products","is_product_in_wishlist_for_current_user"]

    def get_cuurent_user_wishlist(self, obj):
        user = self.context.get('user')
        if user is not None:
            products = obj.products.filter()
            for product in products:
                if Wishlist.objects.filter(product_id=product.id, user=user).exists():
                    return True
                else:
                    return False
        

class RecentViewProductSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    class Meta:
        model = RecentView
        fields ="__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id","name"]

class SearchProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many = False)
    sub_category = SubCategorySerializer(many=False)
    brand = BrandSerializer(many = False)
    images = ImageSerializer(many = True,read_only = True)
    class Meta:
        model = Product
        fields = ["id","name","slug","sku","price","old_price","is_active","is_bestseller","quantity","description","meta_keywords","meta_description","category","sub_category","brand","images"]


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = "__all__"