from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Products(models.Model):
    product_name=models.CharField(null=False,max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to="products/",blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.user.username
    
    
class order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    city=models.CharField()
    address =models.TextField()
    pincode= models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # status = models.CharField(max_length=20, default="Pending")
    
    def __str__(self):
        return self.name
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
   
    def __str__(self):
        return str(self.order.id)