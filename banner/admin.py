from django.contrib import admin
from .models import Banner
# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_or_video', 'caption','description']

admin.site.register(Banner,BannerAdmin)