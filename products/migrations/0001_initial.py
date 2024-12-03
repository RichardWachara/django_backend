# Generated by Django 5.1.3 on 2024-12-02 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the product', max_length=255, unique=True)),
                ('slug', models.SlugField(help_text='Unique_slug for the product', unique=True)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the product')),
                ('price', models.DecimalField(decimal_places=2, help_text='Price of the product', max_digits=10)),
                ('discount_price', models.DecimalField(decimal_places=2, help_text='Discount price of the product', max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0, help_text='Number of items available')),
                ('is_active', models.BooleanField(default=True, help_text='Whether the product is available for purchase')),
                ('image', models.ImageField(blank=True, help_text='The main image of the product', null=True, upload_to='products/images/')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the product was created')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the product was last updated')),
            ],
            options={
                'verbose_name': 'Products',
                'verbose_name_plural': 'Products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/additional_images/')),
                ('alt_text', models.CharField(blank=True, help_text='Alternative text for the image', max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_product_images', to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='additional_images',
            field=models.ManyToManyField(blank=True, help_text='Additional product images', related_name='products_with_images', to='products.productimage'),
        ),
    ]
