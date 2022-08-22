from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product, Image,SubCategory,RecentView,ContactUs

class CategoryAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','is_active','meta_keywords','meta_description','image']    
admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name','category', 'slug','is_active','meta_keywords','meta_description']    
admin.site.register(SubCategory,SubCategoryAdmin)

class BrandAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','meta_keywords','meta_description']
admin.site.register(Brand, BrandAdmin)

class ImageAdmin(admin.StackedInline): 
    model = Image

class ProductAdmin(admin.ModelAdmin): 
    list_display = ["id","name","description","price","quantity","category","sub_category","brand"]   
    inlines = [ImageAdmin]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Image)

class RecentViewAdmin(admin.ModelAdmin):
    list_display = ["id","product","user","views_counter"]

admin.site.register(RecentView, RecentViewAdmin)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display=["id","full_name","email","message"]

