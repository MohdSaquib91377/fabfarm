from django.db import models

# Create your models here.

from account.models import TimeStampModel

class Coupon(TimeStampModel):
    couponCode = models.CharField(max_length = 64)
    percentageFlate = models.BooleanField(default=True)
    discountValue = models.CharField(max_length =64)
    maximumDiscountValue = models.IntegerField()
    couponApplyCount = models.IntegerField(default = 0)
    maxApplyCount = models.IntegerField()
    startDateTime = models.DateTimeField()
    expiryDateTime = models.DateTimeField()
    maxApplyCountPerUser = models.IntegerField(default=1)
    minValue = models.IntegerField()
    status = models.BooleanField(default = True)

    def __str__(self):
        return self.couponCode