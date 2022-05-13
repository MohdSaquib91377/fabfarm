from django.contrib import admin

# Register your models here.
    
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

admin.site.register(Cart,CartAdmin)
