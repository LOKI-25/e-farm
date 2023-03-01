from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=500)
    category_description=models.TextField()
    category_image=models.ImageField(upload_to='images')

    def __str__(self):
        return self.category_name

class Product(models.Model):
    CHOICES = (
    ('kg','Kilogram'),
    ('gm', 'Gram'),
    ('units','units'),
)
    product_name=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product_slug=models.SlugField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    available_quantity=models.IntegerField()
    quantity=models.CharField(max_length=100, choices=CHOICES, default='kg')
    min_quantity_to_fix_price=models.IntegerField()
    price_for_min_quantity=models.IntegerField()
    discount=models.IntegerField(blank=True,null=True,default=0)
    product_image=models.ImageField(upload_to='product_images')
    is_available=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        self.product_slug=slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)
    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price_for_min_quantity * self.quantity


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) 
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject



