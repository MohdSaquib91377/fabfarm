# Generated by Django 4.0.6 on 2022-07-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('couponCode', models.CharField(max_length=64)),
                ('percentageFlate', models.BooleanField(default=True)),
                ('discountValue', models.CharField(max_length=64)),
                ('maximumDiscountValue', models.IntegerField()),
                ('couponApplyCount', models.IntegerField(default=0)),
                ('maxApplyCount', models.IntegerField()),
                ('startDateTime', models.DateTimeField()),
                ('expiryDateTime', models.DateTimeField()),
                ('maxApplyCountPerUser', models.IntegerField(default=1)),
                ('minValue', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]