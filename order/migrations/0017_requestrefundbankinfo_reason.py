# Generated by Django 4.0.6 on 2022-08-12 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_requestrefundbankinfo_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestrefundbankinfo',
            name='reason',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
