from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account.models import TimeStampModel
import PIL.Image
from account.models import *

class Category(TimeStampModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64,unique=True, help_text="Unique value for product page URL,created from name")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=225, help_text="Comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description",max_length=255, help_text="Content for description meta tag")

    class Meta:
        db_table = "Categories"
        ordering = ["-created_at"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
     
    def get_absolute_url(self):
        return ('store:category_view', (), {'slug': self.slug})
    
class Brand(TimeStampModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64,unique=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=225, help_text="Comma-delimited set of SEO keywords for meta tag",null=True)
    meta_description = models.CharField("Meta Description",max_length=255, help_text="Content for description meta tag",null=True)

    class Meta:
        db_table = "Brands"
        ordering = ['-created_at']
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

class Product(TimeStampModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64,unique=True, help_text="Unique value for product page URL,created from name")    
    sku = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords",max_length=225, help_text="Comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description",max_length=255, help_text="Content for description meta tag")
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name="products",null=True)
    #categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products",null=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    
class Image(TimeStampModel):
    image = models.ImageField(upload_to='images/products/main')
    image_caption = models.CharField(max_length=64)
    products = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images', default=None)

    class Meta:
        ordering = ['-created_at']
        db_table = "images"
        verbose_name_plural = "Images"
         
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = PIL.Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)



