# Generated by Django 4.1.1 on 2022-09-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_cart_alter_product_discount_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available_quantity',
            field=models.IntegerField(),
        ),
    ]
