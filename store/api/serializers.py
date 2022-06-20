from unicodedata import category
from rest_framework import serializers

from store.models import *
from account.api.serializers import UserSerializer


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
    category = serializers.CharField(source="category.name", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    maxQuantity = serializers.IntegerField(source = "quantity")
    quantity = serializers.SerializerMethodField("set_qauntity_by_1")
    recently_viwed = serializers.SerializerMethodField("get_recently_viewed_product")
    class Meta:
        model = Product
        fields = ["id","name","slug","sku","price","old_price","is_active","is_bestseller","maxQuantity","quantity","description","meta_keywords","meta_description","category","brand","image","recently_viwed"]
        
    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images,many=True)
        return serializer.data

    def set_qauntity_by_1(self,obj):
        return 1

    def get_recently_viewed_product(self,obj):
        data = dict()
        list = []
        queryset = RecentView.objects.filter(user = self.context['user'])
        for item in queryset:
            data["id"] = item.product.id
            data["name"] = item.product.name
            data["sku"] = item.product.sku
            data["price"] = item.product.price
            data["old_price"] = item.product.old_price
            data["quantity"] = item.product.quantity
            data["images"] = item.product.images.filter().first().image.url
            list.append(data)
            data = {}
        return list
        
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name','products']


