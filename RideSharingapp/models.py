from django.db import models

# Create your models here.

class UserTypeTbl(models.Model):
    type_name = models.CharField(max_length=100,unique=True)

class UserRegisteration(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=100)
    usertype = models.ForeignKey(UserTypeTbl,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile',blank=True,null=True)


class UserTbl(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    empid = models.ForeignKey(UserRegisteration,on_delete=models.CASCADE)