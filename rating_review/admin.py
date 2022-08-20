from django.contrib import admin
from rating_review.models import Rating
# Register your models here.
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product','order_item','rating', 'comment','created_at')