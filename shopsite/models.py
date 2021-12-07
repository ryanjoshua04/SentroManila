from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='shoe_pics')
    quantity = models.IntegerField()
    price = models.IntegerField()

class OrderItems(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email_address = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    message = models.TextField()
    quantity = models.BigIntegerField()
    contact_number = models.BigIntegerField()
    order_itemid = models.IntegerField()
    item_name = models.CharField(max_length=200)
    orderdate = models.DateTimeField(auto_now_add=True)
