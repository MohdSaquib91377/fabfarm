from tkinter import *
from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product, Image

class CategoryAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','description','is_active','meta_keywords','meta_description']    
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','meta_keywords','meta_description']
admin.site.register(Brand, BrandAdmin)

class ProductAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','sku','price','old_price','is_active','is_bestseller','quantity','description','meta_keywords','meta_description']
admin.site.register(Product, ProductAdmin)

class ImageAdmin(admin.ModelAdmin):    
    list_display = ['id', 'image', 'thumbnail','image_caption','products']

admin.site.register(Image, ImageAdmin)

