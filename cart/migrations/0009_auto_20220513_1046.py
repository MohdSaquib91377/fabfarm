# Generated by Django 3.2 on 2022-05-13 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('cart', '0008_remove_cart_total_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-id']},
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='total_item',
            new_name='product_total_price',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='ordered',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]