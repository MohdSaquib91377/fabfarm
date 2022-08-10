from django.db import models
from account.models import TimeStampModel
# Create your models here.
from django.core.exceptions import ValidationError
import PIL.Image
from django.core.files.images import get_image_dimensions




def validate_image(fieldfile_obj):
    file_width, file_height = get_image_dimensions(fieldfile_obj)
    if file_height != 1080 or file_width != 1920:
        raise ValidationError(f"Image size must be {1080} * {1920}")
    return fieldfile_obj



class Page(TimeStampModel):
    page = models.CharField(max_length = 64,null=True, blank=True)

    def __str__(self):
        return self.page

class Banner(TimeStampModel):
    page = models.ForeignKey("Page",on_delete=models.CASCADE,related_name="baners")
    image_or_video = models.FileField(upload_to = "banner",validators=[validate_image])
    caption = models.CharField(max_length=64)
    description = models.TextField()
    class Meta:
        db_table = "banners"
    
    def __str__(self):
        return f"{self.caption}"

