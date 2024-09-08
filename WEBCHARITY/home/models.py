from django.db import models


# Create your models here.

class CharityRegistrationTBL(models.Model):
    phone=models.CharField(max_length=10,primary_key=True)
    charityName=models.CharField(max_length=40,unique=False)
    email=models.CharField(max_length=30,unique=False)
    RegistrationNumber=models.CharField(max_length=40,unique=False)
    address=models.CharField(max_length=50)

class LoginTBL(models.Model):
    RegID=models.CharField(max_length=40)
    Username=models.CharField(max_length=10)
    Pass=models.CharField(max_length=16,unique=False)
    Utype=models.IntegerField(unique=False)
    Status=models.IntegerField(unique=False)


class Donor(models.Model):
    phone=models.CharField(max_length=10,primary_key=True)
    Name=models.CharField(max_length=40)
    email=models.CharField(max_length=30)
    address=models.CharField(max_length=50)

class RequestDetailsTBL(models.Model):
    DetailsId=models.AutoField(primary_key=True)
    CharityRegistrationNumber=models.CharField(max_length=10)
    Amount=models.CharField(max_length=20)
    RequiredDate=models.DateField()
    Details=models.TextField()
    Priority=models.IntegerField(default=1)
    Status=models.IntegerField()

class FinanceManagement(models.Model):
    FinID=models.AutoField(primary_key=True)
    DetailsId=models.IntegerField()
    FromID=models.CharField(max_length=10)
    ToID=models.CharField(max_length=10)
    CrAmount=models.CharField(max_length=20)
    DataAndTime=models.DateTimeField()
    Status=models.IntegerField()