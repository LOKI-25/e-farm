# Generated by Django 4.1.7 on 2023-03-18 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image1',
            field=models.ImageField(blank=True, null=True, upload_to='product_images1'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image2',
            field=models.ImageField(blank=True, null=True, upload_to='product_images2'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image3',
            field=models.ImageField(blank=True, null=True, upload_to='product_images3'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image4',
            field=models.ImageField(blank=True, null=True, upload_to='product_images4'),
        ),
    ]
