from django.db import models
from django.contrib.auth.models import User
# from .models import Product

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vendor_number = models.CharField(max_length=200, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_stars = models.IntegerField(null=True, blank=True, default=0)
    product_units = models.IntegerField()
    product_image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)
    product_description = models.TextField(default=' ', null=True, blank=True)

    def __str__(self):
        return self.product_name
    
class VendorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    campus = models.CharField(max_length=200, null=True, blank=True)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.IntegerField()
    order_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_name 
    

