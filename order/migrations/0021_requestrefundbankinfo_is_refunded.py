# Generated by Django 4.0.6 on 2022-08-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_receivereturn_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestrefundbankinfo',
            name='is_refunded',
            field=models.BooleanField(default=False),
        ),
    ]
