# Generated by Django 4.1.1 on 2022-09-13 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_product_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='price_for_min_quantity',
        ),
        migrations.AddField(
            model_name='product',
            name='available_quantity',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='min_quantity',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.CharField(choices=[('kg', 'Kilogram'), ('gm', 'Gram'), ('packet', 'Packet')], default='kg', max_length=6),
        ),
    ]
