from statistics import mode
from turtle import ondrag

from django.contrib.auth.models import User
from django.db import models
from pyexpat import model

# Create your models here.

class Customer(models.Model):
    customer = models.OneToOneField(User,models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(null=True,blank=True)
    isdigital = models.BooleanField(default=False,blank =False,null=True)
    
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null= True,blank = True)
    date = models.DateTimeField(auto_now_add=True)
    statuses = (
    ("Pending","Pending"),
    ("Shipped","Shipped"),
    ("Completed","Completed")
    )
    complete = models.BooleanField(default=False)

    status = models.CharField(max_length=255,
                  choices=statuses,
                  default="Pending")
    transactionID = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.id)
    
    @property 
    def get_items_quantity(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total
    @property 
    def get_items_price(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total

    # @property
    # def shipping(self):
    #     orderItem = self.orderitem_set.all()
    #     s = True
    #     for item in orderItem:
    #         if item.

   
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null= True,blank = True)
    Order = models.ForeignKey(Order,on_delete=models.SET_NULL,null= True,blank = True)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class Shipping(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null= True,blank = True)
    Order = models.ForeignKey(Order,on_delete=models.SET_NULL,null= True,blank = True)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
     
