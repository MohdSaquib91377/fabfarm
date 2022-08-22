
from rating_review.models import *
from rest_framework import serializers
class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True,source = "user.fullname")
    product = serializers.PrimaryKeyRelatedField(read_only = True)
    created_at = serializers.SerializerMethodField("get_formated_date")
    class Meta:
        model = Rating
        fields = ["rating","comment","order_item","user","product","created_at"]
        extra_fields = {"comment":{"required": False,"allow_null": True},
                        "product":{"required": False,"allow_null": True},
                        "user":{"required": False,"allow_null": True},
                        "product":{"required": False,"allow_null": True},
                        "created_at":{"required": False,"allow_null":True}
                        
                        }
    
    def get_formated_date(self,obj):
        date = obj.created_at.strftime("%b,%Y")
        return date
