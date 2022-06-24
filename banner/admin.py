from django.contrib import admin
from .models import Banner,Page
# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'page']

admin.site.register(Page,PageAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_or_video', 'caption','description']

admin.site.register(Banner,BannerAdmin)