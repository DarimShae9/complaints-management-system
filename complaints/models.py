from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    nip = models.CharField(max_length=16, primary_key=True)
    adress = models.CharField(max_length=64, null=True, blank=True)


USER_ROLE = (
    ('1', 'admin'),
    ('2', 'owner'),
    ('3', 'employer')
)


class MyUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user_custom_role = models.IntegerField(choices=USER_ROLE, default=2)

STATUS_LIST = (
    (1, 'new'),
    (2, 'during'),
    (3, 'rejected'),
    (4, 'done'),
)



class Product(models.Model):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.FloatField(null=True)


class Order(models.Model):
    number = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_LIST, default=1)
    creation_date = models.DateTimeField(default=datetime.now())
    modification_date = models.DateTimeField(default=datetime.now())
    product = models.ManyToManyField(Product)


class Message(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    creation_date = models.DateTimeField(default=datetime.now())

