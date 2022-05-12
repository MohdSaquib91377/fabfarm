from django.contrib import admin

# Register your models here.
    
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','ordered','total_price','total_item','user']

admin.site.register(Cart,CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','cart','product','quantity']

admin.site.register(CartItem,CartItemAdmin)
