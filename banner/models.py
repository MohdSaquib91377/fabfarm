from django.db import models
from account.models import TimeStampModel
# Create your models here.

class Banner(TimeStampModel):
    PAGES_CHOICES = (
        
        ("Home","Home"),
        ("About","About"),
        ("Contact","Contact"),
        ("Filter","Filter"),
        
        )
    image_or_video = models.FileField(upload_to = "banner")
    caption = models.CharField(max_length=64)
    description = models.TextField()
    page = models.CharField(choices = PAGES_CHOICES,default = "Home",max_length = 64)
    class Meta:
        db_table = "banners"
    
    def __str__(self):
        return f"{self.caption}"