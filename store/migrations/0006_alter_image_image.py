# Generated by Django 4.0.6 on 2022-08-26 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='fabfarm.jpg', upload_to='images/products/main/'),
        ),
    ]
