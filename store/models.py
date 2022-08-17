from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account.models import TimeStampModel
import PIL.Image
from account.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

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

class SubCategory(TimeStampModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64,unique=True, help_text="Unique value for product page URL,created from name")
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=225, help_text="Comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description",max_length=255, help_text="Content for description meta tag")
    category = models.ForeignKey("Category",on_delete = models.CASCADE,related_name = "sub_categories",null= True)
    class Meta:
        db_table = "SubCategories"
        ordering = ["-created_at"]
        verbose_name_plural = "SubCategories"

    def __str__(self):
        return self.name
     
    def __str__(self) -> str:
        return f"{self.name} -> {self.category.name}"
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
    price = models.FloatField(validators=[MinValueValidator(0.0)],default=0.0)
    old_price = models.FloatField(validators=[MinValueValidator(0.0)],default=0.0,blank=True)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords",max_length=225, help_text="Comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description",max_length=255, help_text="Content for description meta tag")
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name="products",null=True)
    sub_category = models.ForeignKey('SubCategory',on_delete=models.CASCADE,related_name="products",null=True)
    #categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products",null=True)
    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} -> {self.name} -> {self.sub_category.name} -> {self.category.name}"

    def clean(self):
        sub_category_list = SubCategory.objects.filter(category = self.category).values_list("id",flat = True)
        if not self.sub_category_id in sub_category_list:
            raise ValidationError("Sub Category does not match for category")
        super(Product, self).clean()


class Image(TimeStampModel):
    image = models.ImageField(upload_to='images/products/main/')
    image_caption = models.CharField(max_length=64)
    products = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images', default=None)

    class Meta:
        ordering = ['-created_at']
        db_table = "images"
        verbose_name_plural = "Images"
         
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = PIL.Image.open(self.image.path)
        output_size = (500,400)
        img.thumbnail(output_size)
        img.save(self.image.path)

class RecentView(TimeStampModel):
    user = models.ForeignKey("account.CustomUser",on_delete=models.CASCADE,related_name="recent_views")
    product = models.ForeignKey("Product",on_delete=models.CASCADE,related_name="recent_views")
    views_counter = models.IntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]


class ContactUs(TimeStampModel):
    full_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    message = models.TextField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "contact_us"
        verbose_name_plural = "Contact us"