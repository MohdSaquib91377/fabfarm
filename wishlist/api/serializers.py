from rest_framework import serializers
from wishlist.models import Wishlist
from account.api.serializers import UserSerializer
from store.api.serializers import ProductsSerializer

class WishListCreateDeleteSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = Wishlist
        fields = ["product_id"]
        extra_kwargs = {"user": {"required": False, "allow_null": True},"product": {"required": False, "allow_null": True}}


class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductsSerializer()
    class Meta:
        model = Wishlist
        fields = "__all__"