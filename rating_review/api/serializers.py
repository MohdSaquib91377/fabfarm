
from rating_review.models import *
from rest_framework import serializers
class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["rating","comment","order_item","user"]
        extra_fields = {"comment":{"required": False,"allow_null": True},"product":{"required": False,"allow_null": True},"user":{"required": False,"allow_null": True}}
    
  
    