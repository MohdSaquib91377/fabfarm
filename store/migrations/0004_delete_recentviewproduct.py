# Generated by Django 4.0.5 on 2022-06-21 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_recentview_recentviewproduct_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecentViewProduct',
        ),
    ]
