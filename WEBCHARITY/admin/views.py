from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse,JsonResponse, response
import sys,os
"""
sys.path.append(os.path.abspath('../home'))
from ..home import models
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt

def CharityReg(request):
    data={}
    ob= models.Donor.objects.all()
    data1={}
    for i in ob:
        data1["name"]=i.Name
        data1["phone"]=i.phone
    data.update(data1)    
    return render(request,'CharityReg.html',data)
"""