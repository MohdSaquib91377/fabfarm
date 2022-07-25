from email.policy import default
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

from account.models import TimeStampModel

class Coupon(TimeStampModel):
    couponCode = models.CharField(max_length = 64)
    percentageFlate = models.BooleanField(default=True)
    discountValue = models.CharField(max_length =64)
    maximumDiscountValue = models.PositiveIntegerField()
    couponApplyCount = models.PositiveIntegerField(default = 1)
    maxApplyCount = models.PositiveIntegerField(default=1)
    startDateTime = models.DateTimeField()
    expiryDateTime = models.DateTimeField()
    maxApplyCountPerUser = models.PositiveIntegerField(default=1)
    minValue = models.PositiveIntegerField(default = 1)
    status = models.BooleanField(default = True)

    def __str__(self):
        return self.couponCode

    def clean(self):
        if self.startDateTime and self.expiryDateTime is not None:
            if self.startDateTime > self.expiryDateTime:
                raise ValidationError("startDateTime must be less than expiryDateTime")
        super(Coupon, self).clean()