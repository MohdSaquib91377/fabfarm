# Generated by Django 4.0.6 on 2022-08-30 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0029_requestrefunditem_recieved_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestrefunditem',
            name='recieved_product',
        ),
    ]
