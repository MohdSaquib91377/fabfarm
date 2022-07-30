# Generated by Django 4.0.6 on 2022-07-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_mobile_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mobile',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]