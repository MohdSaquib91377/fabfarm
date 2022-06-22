from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product, Image,SubCategory

class CategoryAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','is_active','meta_keywords','meta_description']    
admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name','category', 'slug','is_active','meta_keywords','meta_description']    
admin.site.register(SubCategory, CategoryAdmin)
class BrandAdmin(admin.ModelAdmin):    
    list_display = ['id', 'name', 'slug','meta_keywords','meta_description']
admin.site.register(Brand, BrandAdmin)

class ImageAdmin(admin.StackedInline): 
    model = Image

class ProductAdmin(admin.ModelAdmin):    
    inlines = [ImageAdmin]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Image)

<<<<<<< HEAD

=======
>>>>>>> origin/sub-category
