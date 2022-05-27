from rest_framework import serializers
from wishlist.models import Wishlist
from account.api.serializers import UserSerializer
from store.api.serializers import ProductsSerializer

class WishListCreateDeleteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Wishlist
        fields = ["user","product"]

class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductsSerializer()
    class Meta:
        model = Wishlist
        fields = "__all__"