from django.db import models

# Create your models here.
class Account(models.Model):
  name = models.CharField(max_length=32)
  DOB = models.DateField()
  mail = models.EmailField(default='demofbh@gmail.com')
  aadhar = models.CharField(unique=True,max_length=12)
  pan = models.CharField(max_length=10, unique=True)
  mobile = models.IntegerField(unique=True)
  address = models.TextField()
  acc = models.BigAutoField(primary_key=True)
  balance = models.DecimalField(decimal_places=2,max_digits=12, default=1000.0)
  pin = models.IntegerField(default=0)
  otp = models.IntegerField(default=0)
