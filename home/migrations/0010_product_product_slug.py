# Generated by Django 4.1.1 on 2022-09-14 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_slug',
            field=models.SlugField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
