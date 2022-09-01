from rest_framework.response import Response
from rest_framework import serializers
from order.models import Order,OrderItem,ReturnRefundPolicy,RequestRefundItem
from account.api.serializers import *
from store.api.serializers import *
from store.models import *
from django.utils import timezone
from datetime import timedelta
from rating_review.api.serializers import *

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    coupon = serializers.PrimaryKeyRelatedField(read_only = True)
    address = serializers.SerializerMethodField("get_order_address")

    class Meta:
        model = Order
        fields = ["payment_mode","user","coupon","user_address","address"]
    def get_order_address(self,obj):
        serializer = UserAddressSerializer(obj.user_address).data
        return serializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    order = serializers.PrimaryKeyRelatedField(read_only = True)
    payment_mode = serializers.SerializerMethodField("get_order_payment_mode")
    return_refund_validaty = serializers.SerializerMethodField("check_return_refund_validaty")
    order_item_rating = serializers.SerializerMethodField("get_order_item_rating")
    class Meta:
        model = OrderItem
        fields = "__all__"  

    def get_order_payment_mode(self,obj):
        if obj.order.payment_mode in ["COD","cod"]:
            return "Cash on delivery"
        else:
            return "Razorpay"
    
    def check_return_refund_validaty(self,obj):
        # get refund validaty
        object = ReturnRefundPolicy.objects.filter().first()
        days = int(object.return_refund_timestamp.split(" ")[0])
        order_date = obj.order.created_at + timedelta(days)
        if timezone.now() > order_date:
            return {
                "status":False,
                "message":"Return/Refund policy expire"
            }  
        else:
            return {
            "status":True,
            "message":f"Return/Refund has validaty {days} days of it's purchase date"
            }      
    
    def get_order_item_rating(self,obj):
        rating_obj = obj.ratings.filter(order_item__id = obj.id,user__id = obj.order.user.id).first()
        if rating_obj:
            return {
                "ratings": rating_obj.rating,
                "id":rating_obj.id,
                "review":rating_obj.comment
            }

class OrderItemDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    order = OrderSerializer()
    payment_mode = serializers.SerializerMethodField("get_order_payment_mode")
    order_item_rating = serializers.SerializerMethodField("get_order_item_rating")

    class Meta:
        model = OrderItem
        fields = "__all__"  

    def get_order_payment_mode(self,obj):
        if obj.order.payment_mode in ["COD","cod"]:
            return "Cash on delivery"
        else:
            return "Razorpay"
    def get_order_item_rating(self,obj):
        queryset = Rating.objects.filter(order_item=obj,user = obj.order.user)
        if queryset:
            serializer = ProductRatingSerializer(queryset,many=True).data
            return serializer
        return None

    def get_order_item_rating(self,obj):
        rating_obj = obj.ratings.filter(order_item__id = obj.id,user__id = obj.order.user.id).first()
        if rating_obj:
            return {
                "ratings": rating_obj.rating,
                "id":rating_obj.id,
                "review":rating_obj.comment
            }

# admin side
class OrderItemIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id"]



class RequestRefundItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestRefundItem   
        fields = ["order_item","fund_accounts"]            


class FundAccoutSerializer(serializers.ModelSerializer):
    confirm_account_number = serializers.IntegerField(required=False)

    class Meta:
        model = FundAccout
        fields = ["id","ifsc","name","account_number","confirm_account_number"]
        extra_kwargs = {

                        "user":{"required":False, "allow_null":True},
                        "contact_id":{"required":False, "allow_null":True},
                        "razorpay_fund_id":{"required":False, "allow_null":True},
                        "account_type":{"required":False, "allow_null":True},
                        "active":{"required":False, "allow_null":True},
                        "bank_name":{"required":False, "allow_null":True},
                        "confirm_account_number":{"required":False, "allow_null":True},
                        "id":{"required":False, "allow_null":True},


                        }
