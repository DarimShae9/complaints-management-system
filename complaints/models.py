from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    nip = models.CharField(max_length=9, primary_key=True)
    adress = models.CharField(max_length=64, null=True, blank=True)


USER_ROLE = (
    ('1', 'admin'),
    ('2', 'owner'),
    ('3', 'employer')
)


class MyUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user_custom_role = models.IntegerField(choices=USER_ROLE, default=2)


class Status(models.Model):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Order(models.Model):
    number = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
