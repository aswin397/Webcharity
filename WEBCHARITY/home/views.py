from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, response
from .models import *
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import FileResponse



######## HOME ########################################




@csrf_exempt

def Index(request):
    request.session.flush()
    return render(request,'index.html')


@csrf_exempt

def forgotPassword2(request):
    uname=request.GET.get("uname")
    pswrd=request.GET.get("pswrd")
    Utype=request.GET.get("Utype")
    uid=request.GET.get("uid")
    try:
        if int(Utype)==2:
            ob=CharityRegistrationTBL.objects.get(phone=uid,charityName=uname)
            oj=LoginTBL.objects.get(RegID=ob.phone,Username=ob.phone,Utype=2)
            oj.Pass=pswrd
            ob.save()
            data={"status":1}
            return JsonResponse(data,safe=False)
        elif int(Utype==3):
            ob=Donor.objects.get(phone=uid,Name=uname)
            oj=LoginTBL.objects.get(RegID=ob.phone,Username=ob.phone,Utype=3)
            oj.Pass=pswrd
            ob.save()
            data={"status":1}
            return JsonResponse(data,safe=False)
    except Exception as e:
        data={"status":0}
        return JsonResponse(data,safe=False)

@csrf_exempt

def forgotPassword(request):
    return render(request,'forgotPassword.html')


@csrf_exempt

def about(request):
    return render(request,'about.html')



@csrf_exempt

def CharityReg(request):
    return render(request,'CharityReg.html',{})

@csrf_exempt

def DonorReg(request):
    return render(request,'DonorReg.html',{})

@csrf_exempt

def Login(request):
    return render(request,'login.html')
@csrf_exempt

def adminhome(request):
    return render(request,'admin/adminhome.html',{})

@csrf_exempt

def charityhome(request):
    ph=request.session['UserName']
    ob=CharityRegistrationTBL.objects.get(phone=ph)
    return render(request,'charity/charityhome.html',{"Name":ob.charityName})

@csrf_exempt

def donorhome(request):
    raised=0
    num=0
    selected_rows = FinanceManagement.objects.filter(FromID=request.session['UserName'])
    for i in selected_rows:
        raised=raised+int(i.CrAmount)
        num=num+1
    return render(request,'donor/donorhome.html',{"part":num,"amt":raised})


@csrf_exempt

def CheckLogin(request):
    uname=request.GET.get("uname")
    pswrd=request.GET.get("pswrd")
    Utype=request.GET.get("Utype")
    print(uname,pswrd)
    if(uname=="admin" and pswrd=="admin" and Utype=="1"):
        data={"status":1}
        return JsonResponse(data,safe=False)
    else:
        try:
            ob=LoginTBL.objects.get(Username=uname,Pass=pswrd,Utype=Utype)
            request.session['UserName'] =ob.RegID
            if ob.Utype==2:
                data={"status":2}
                return JsonResponse(data,safe=False)
            if ob.Utype==3:
                data={"status":3}
                return JsonResponse(data,safe=False)
        except Exception as e:
           data={"status":0}
           return JsonResponse(data,safe=False)
 

@csrf_exempt

def RegCharity(request):
    name=request.POST.get("name")
    phone=request.POST.get("phone")
    registration=request.POST.get("registration")
    email=request.POST.get("email")
    address=request.POST.get("address")
    password=request.POST.get("password")
    data={}
    if registration==None:
        registration="NON CHARITY"
    print(registration)
    try:
        CharityRegistrationTBL.objects.create(phone=phone,charityName=name,email=email,RegistrationNumber=registration,address=address)
        LoginTBL.objects.create(RegID=phone,Username=phone,Pass=password,Utype=2,Status=0)
        data={"msg":"Successfully Registread"}
    except IntegrityError:
      
        data={"msg":"User Already Exist"}
        
        print(data)
        return render(request,'CharityReg.html',data)
    except Exception as e:
        data={"msg":"Submission failed"}
        print(e)
        return render(request,'CharityReg.html',data)
    
    return render(request,'CharityReg.html',data)




@csrf_exempt

def RegDonor(request):
    Name=request.POST.get("name")
    phone=request.POST.get("phone")
    email=request.POST.get("email")
    address=request.POST.get("address")
    password=request.POST.get("password")
    data={}
    try:
        Donor.objects.create(Name=Name,phone=phone,email=email,address=address)
        LoginTBL.objects.create(RegID=phone,Username=phone,Pass=password,Utype=3,Status=1)
        data={"msg":"Successfully Registread"}
    except IntegrityError:
      
        data={"msg":"User Already Exist"}
        return render(request,'DonorReg.html',data)
    except Exception as e:
        data={"msg":"Submission failed"}
        print(e)
        return render(request,'DonorReg.html',data)
    
    return render(request,'DonorReg.html',data)
    
    


#######################################  ADMIN ####################################################################################################################



@csrf_exempt

def ViewUser(request):
    data={}
    ob= Donor.objects.all()
    data1={}
    datalist=[]
    for i in ob:
        user_data = {
            "name": i.Name,
            "phone": i.phone
        }
        datalist.append(user_data)
    data["data"] = datalist   
    print(data) 
    return render(request,'admin/ViewDonor.html',data)



@csrf_exempt

def ViewUser2(request):
    phone_number = request.GET.get('phone')
    ob=Donor.objects.get(phone=phone_number)
    user_data = {
        "name": ob.Name,
        "phone": ob.phone,
        "email": ob.email,
        "address":ob.address,
        }
    data={}
    obj= FinanceManagement.objects.filter(FromID=ob.phone)
    data1={}
    datalist=[]
    for i in obj:
        n=CharityRegistrationTBL.objects.get(phone=i.ToID)
        user_data1 = {
            "name": n.charityName,
            "date": i.DataAndTime,
            "amt": i.CrAmount,
            "TID": i.FinID,
            "PDF": "INVOICE"+str(i.FinID),
        }
        datalist.append(user_data1)
    user_data["user"]=datalist
    return render(request,'admin/ViewDonor2.html',user_data)   



@csrf_exempt

def ApproveCharity(request):
    try:
        data={}
        ob= CharityRegistrationTBL.objects.all()
        data1={}
        datalist=[]
        for i in ob:
            if LoginTBL.objects.filter(RegID=i.phone,Status='0',Utype=2):
                user_data = {
                    "name": i.charityName,
                    "Reg": i.phone
                }
                datalist.append(user_data)
        data["data"] = datalist   
        print(data) 
        return render(request,'admin/ApproveCharity.html',data)
    except Exception as e:
        data={}
        return render(request,'admin/ApproveCharity.html',data)

@csrf_exempt

def ApproveCharity2(request):
    phone_number = request.GET.get('phone')
    user_data={}
    ob=CharityRegistrationTBL.objects.get(phone=phone_number)
   
    type=""
    if ob.RegistrationNumber=="NON CHARITY":type="For Personal Purpose" 
    else: type="Charity"
    user_data = {
        "name": ob.charityName,
        "phone": ob.phone,
        "email": ob.email,
        "address":ob.address,
        "RegNumber":ob.RegistrationNumber,
        "Type": type,
        }
        
    return render(request,'admin/ApproveCharity2.html',user_data)   


@csrf_exempt

def ApproveCharity3(request):
    P=request.POST.get('myInput')

    print(P)
    ob=LoginTBL.objects.get(Utype=2,RegID=P)
    ob.Status="1" 
    ob.save()
    return render(request,'admin/ApproveCharity.html',{"msg":" APPROVED SUCESSFULLY "})






@csrf_exempt

def ApproveDonation(request):
    try:
        data={}
        ob= RequestDetailsTBL.objects.all()
        datalist=[]
        for i in ob:
            if i.Status==0:
                o=CharityRegistrationTBL.objects.get(phone=i.CharityRegistrationNumber)
                user_data = {
                    "name": o.charityName,
                    "Reg": i.DetailsId
                }
                datalist.append(user_data)
                data["data"] = datalist   
        print(data) 
        return render(request,'admin/ApproveDonation.html',data)
    except Exception as e:
        data={}
        return render(request,'admin/ApproveDonation.html',data)





@csrf_exempt

def ApproveDonation2(request):
    RequestID = request.GET.get('phone')
    user_data={}
    ob=RequestDetailsTBL.objects.get(DetailsId=RequestID)
    o=CharityRegistrationTBL.objects.get(phone=ob.CharityRegistrationNumber)
    type=""
    if o.RegistrationNumber=="NON CHARITY":type="For Personal Purpose" 
    else: type="Charity"


    
    pdf_file_path1=RequestID
    file_path = str(pdf_file_path1) + '.pdf'
    pdf_file_path = os.path.join(settings.BASE_DIR, file_path)

    if os.path.exists(pdf_file_path):
        print("SSSSSSSSSS")
    print(file_path)
    if 'Pdf' in request.session:
        del request.session['Pdf']
   
    request.session['Pdf'] =pdf_file_path
    user_data = {
        "name": o.charityName,
        "phone": o.phone,
        "DetailsId": ob.DetailsId,
        "Amount":ob.Amount,
        "email":o.email,
        "RequiredDate":ob.RequiredDate,
        "Details":ob.Details,
        "address":o.address,
        "type":type,
        "pdf_file_path": file_path,
        }
        
    return render(request,'admin/ApproveDonation2.html',user_data)   





@csrf_exempt

def ApproveDonation3(request):
    DetailID=request.POST.get('myInput')
    Amount=request.POST.get('amount')
    Priority=request.POST.get('Priority')
    if 'Approve' in request.POST.get('action'):
        ob=RequestDetailsTBL.objects.get(DetailsId=DetailID)
        ob.Priority=Priority
        ob.Amount=Amount
        ob.Status="1" 
        ob.image='img'+str(DetailID)+'.jpg'
        ob.save()
        return render(request,'admin/ApproveDonation.html',{"msg":" APPROVED SUCESSFULLY "})
    elif 'Cancel' in request.POST.get('action'):
        ob=RequestDetailsTBL.objects.get(DetailsId=DetailID)
        ob.Status="2"   # 2 denots the request is blocked permentently
        ob.save()
        
        return render(request,'admin/ApproveDonation.html',{"msg":" REMOVED SUCESSFULLY "})

    else:
        return render(request,'admin/ApproveDonation.html',{"msg":" Failed "})



@csrf_exempt
def pdfDonationViewAdmin(request):
    FIN=request.GET.get('FID')
    FIN="INVOICE"+str(FIN)+".pdf"
    print(FIN)
    return render(request,'admin/pdfDonationViewAdmin.html',{"PDF":FIN})








@csrf_exempt

def viewcharities(request):
    try:
        data={}
        ob= CharityRegistrationTBL.objects.all()
        data1={}
        datalist=[]
        for i in ob:
            if LoginTBL.objects.filter(RegID=i.phone,Status='1',Utype=2):
                user_data = {
                    "name": i.charityName,
                    "Reg": i.phone
                }
                datalist.append(user_data)
        data["data"] = datalist   
        print(data) 
        return render(request,'admin/viewcharities.html',data)
    except Exception as e:
        data={}
        print(e)
        return render(request,'admin/viewcharities.html',data)
    



from django.db.models import Sum
@csrf_exempt

def viewcharities2(request):
    phone_number = request.GET.get('Reg')
    ob=CharityRegistrationTBL.objects.get(phone=phone_number)
    user_data = {
        "name": ob.charityName,
        "phone": ob.phone,
        "email": ob.email,
        "address":ob.address,
        "RegistrationNumber":ob.RegistrationNumber,
        }
    
    priority_mapping = {
    1: "High",
    2: "Medium",
    3: "Low"
    }

    data={}
    obj= RequestDetailsTBL.objects.filter(CharityRegistrationNumber=ob.phone)
    data1={}
    datalist=[]
    for i in obj:
        total_cramount = FinanceManagement.objects.filter(DetailsId=i.DetailsId).aggregate(sum_cramount=Sum('CrAmount'))['sum_cramount']
        if total_cramount is None:
            total_cramount = 0.0

        user_data1 = {
            "DetailsId": i.DetailsId,
            "Amount": i.Amount,
            "RequiredDate": i.RequiredDate,
            "Priority": priority_mapping.get(i.Priority, "Unknown"),
            "Status": "Active" if int(i.Status) == 1 else "Inactive",
            "raised":total_cramount

        }
        datalist.append(user_data1)
    user_data["user"]=datalist
    return render(request,'admin/viewcharities2.html',user_data)   



@csrf_exempt

def DonationStatusAdmin(request):
    try:
        data={}
        ob= RequestDetailsTBL.objects.filter(Status=1)
        data1={}
        datalist=[]
        for i in ob:
            n=CharityRegistrationTBL.objects.get(phone=i.CharityRegistrationNumber)
            user_data = {
                    "name": n.charityName,
                    "Reg": i.DetailsId,
                    "Details":i.Details
            }
            datalist.append(user_data)
        data["data"] = datalist   
        print(data) 
        return render(request,'admin/DonationStatusAdmin.html',data)
    except Exception as e:
        data={}
        print(e)
        return render(request,'admin/DonationStatusAdmin.html',data) 

@csrf_exempt

def DonationStatusAdmin2(request):  
    DetailsId = request.GET.get('ReqID')
    priority_mapping = {
    1: "High",
    2: "Medium",
    3: "Low"
    }
    total_cramount = FinanceManagement.objects.filter(DetailsId=DetailsId).aggregate(sum_cramount=Sum('CrAmount'))['sum_cramount']
    if total_cramount is None:
            total_cramount = 0.0
    ob=RequestDetailsTBL.objects.get(DetailsId=DetailsId)
    o=CharityRegistrationTBL.objects.get(phone=ob.CharityRegistrationNumber)
    user_data ={
        "DetailsId": ob.DetailsId,
        "CharityRegistrationNumber": ob.CharityRegistrationNumber,
        "CharityName":o.charityName,
        "Amount": ob.Amount,
        "RequiredDate":ob.RequiredDate,
        "Details":ob.Details,
        "Priority":priority_mapping.get(ob.Priority, "Unknown"),
        "Status":"Active" if int(ob.Status) == 1 else "Inactive",
        "TotalC":total_cramount,
        "Shortage":int(ob.Amount)-int(total_cramount)
    
        }
    
    data={}
    obj= FinanceManagement.objects.filter(DetailsId=ob.DetailsId)
    data1={}
    datalist=[]
    for i in obj:

        n=Donor.objects.get(phone=i.FromID)
        user_data1 = {
            "FinID": i.FinID,
            "FromName": n.Name,
            "CrAmount": i.CrAmount,
            "DataAndTime": i.DataAndTime,

        }
        datalist.append(user_data1)
    user_data["user"]=datalist
    print(user_data)
    return render(request,'admin/DonationStatusAdmin2.html',user_data)   







#######################################  CHARITY ####################################################################################################################





@csrf_exempt

def DonationRequesthtml(request):
    return render(request,'charity/DonationRequesthtml.html',{})

@csrf_exempt

def DonationRequest(request):
    try:
       RegID=request.session.get('UserName', None)
       if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        details = request.POST.get('details')
        pdf_file = request.FILES.get('file')
        #try:
        ob=RequestDetailsTBL.objects.create(CharityRegistrationNumber=RegID,Amount=amount,RequiredDate=date,Details=details,Status=0)
        new_name=str(ob.DetailsId)
        print(new_name)
            # Read the content of the uploaded file as bytes
        file_content = pdf_file.read()
            
            # Construct the file path with the desired file extension (.pdf)
        file_path = "static/"+new_name + '.pdf'

       
            # Open the file in binary write mode and write the content
        with open(file_path, 'wb') as file_to_save:
            file_to_save.write(file_content)
            
        return render(request,'charity/DonationRequesthtml.html',{"msg":" Requested Successfully. Our team will contact you"})
    except Exception as e:
        print(e)
        return render(request,'charity/DonationRequesthtml.html',{"msg":" Failed "})




@csrf_exempt

def MyProfileCharity(request):
    phone_number = request.session['UserName']
    a=True
    if a:
  
        ob = CharityRegistrationTBL.objects.get(phone=phone_number)
        
       
        user = {
            'phone':ob.phone,
            'charityName': ob.charityName,
            'email': ob.email,
            'RegistrationNumber': ob.RegistrationNumber,
            'address': ob.address,
        }
        
        return render(request,'charity/MyProfileCharity.html',user)
    else:
        
        return render(request, 'charity/MyProfileCharity.html',{})    


@csrf_exempt

def RequetStatusCharity(request):
    try:
        phone_number = request.session['UserName']
        data={}
        ob= RequestDetailsTBL.objects.filter(CharityRegistrationNumber=phone_number)
        data1={}
        datalist=[]
        for i in ob:
            user_data = {
                    "Reg": i.DetailsId,
                    "Details":i.Details,
                    "status":"Active" if int(i.Status) == 1 else "Inactive",
            }
            datalist.append(user_data)
        data["data"] = datalist   
        print(data) 
        return render(request,'charity/RequetStatusCharity.html',data)
    except Exception as e:
        data={}
        print(e)
        return render(request,'charity/RequetStatusCharity.html',data) 



def RequetStatusCharity2(request):
    DetailsId = request.GET.get('ReqID')
    priority_mapping = {
    1: "High",
    2: "Medium",
    3: "Low"
    }
    total_cramount = FinanceManagement.objects.filter(DetailsId=DetailsId).aggregate(sum_cramount=Sum('CrAmount'))['sum_cramount']
    if total_cramount is None:
            total_cramount = 0.0
    ob=RequestDetailsTBL.objects.get(DetailsId=DetailsId)
    user_data ={
        "DetailsId": ob.DetailsId,
        "Amount": ob.Amount,
        "RequiredDate":ob.RequiredDate,
        "Details":ob.Details,
        "Priority":priority_mapping.get(ob.Priority, "Unknown"),
        "Status":"Active" if int(ob.Status) == 1 else "Inactive",
        "TotalC":total_cramount,
        "Shortage":int(ob.Amount)-int(total_cramount)
    
        }
    
    data={}
    obj= FinanceManagement.objects.filter(DetailsId=ob.DetailsId)
    data1={}
    datalist=[]
    for i in obj:

        n=Donor.objects.get(phone=i.FromID)
        user_data1 = {
            "FinID": i.FinID,
            "FromName": n.Name,
            "CrAmount": i.CrAmount,
            "DataAndTime": i.DataAndTime,

        }
        datalist.append(user_data1)
    user_data["user"]=datalist
    print(user_data)
    return render(request,'charity/RequetStatusCharity2.html',user_data)   





@csrf_exempt
def pdfDonationViewCharity(request):
    FIN=request.GET.get('FID')
    FIN="INVOICE"+str(FIN)+".pdf"
    print(FIN)
    return render(request,'charity/pdfDonationViewCharity.html',{"PDF":FIN})






###############################################################    DONOR   #####################################################################################################

from datetime import date
from django.db.models import Q


@csrf_exempt

def ViewAll(request):
    data={}
    cases_data=[]
    today = date.today()

    
    filtered_rows = RequestDetailsTBL.objects.filter(Q(Priority=1) | Q(Priority=2) | Q(Priority=3),Status="1",RequiredDate__gt=today).order_by('Priority') 
    for row in filtered_rows:
        print(row.DetailsId,row.Priority, row.Status, row.RequiredDate)
    for i in filtered_rows:
        raised=0
        selected_rows = FinanceManagement.objects.filter(DetailsId=i.DetailsId,Status=1)
        for row in selected_rows:
            raised=raised+int(row.CrAmount)
        if raised>=int(i.Amount):
            pass
        else:
            data1 =  {
                'image': 'case'+str(60)+'.png',
                'title': i.Details,
                'percentage':(raised*100)//int(i.Amount),
                'raised': raised,
                'goal': i.Amount,
                'id':i.DetailsId,
                 }
     
            cases_data.append(data1)
        
        data["data"]=cases_data 
    print(data) 
    return render(request,'donor/ViewAll.html',data)

@csrf_exempt

def ViewAll2(request):
    RequestID = request.GET.get('id')
    user_data={}
    ob=RequestDetailsTBL.objects.get(DetailsId=RequestID)
    o=CharityRegistrationTBL.objects.get(phone=ob.CharityRegistrationNumber)
    type=""
    if o.RegistrationNumber=="NON CHARITY":type="For Personal Purpose" 
    else: type="Charity"


    
    pdf_file_path1=RequestID
    file_path = str(pdf_file_path1) + '.pdf'
    pdf_file_path = os.path.join(settings.BASE_DIR, file_path)

    if os.path.exists(pdf_file_path):
        print("PDF EXISTING")
    print(file_path)
    if 'Pdf' in request.session:
        del request.session['Pdf']
   
    request.session['Pdf'] =pdf_file_path
    user_data = {
        "name": o.charityName,
        "phone": o.phone,
        "DetailsId": ob.DetailsId,
        "Amount":ob.Amount,
        "email":o.email,
        "RequiredDate":ob.RequiredDate,
        "Details":ob.Details,
        "address":o.address,
        "type":type,
        "pdf_file_path": file_path,
        }
        
    return render(request,'donor/ViewAll2.html',user_data)  


@csrf_exempt

def ViewAll3(request):
    RequestID =request.POST.get('myInput')
    CharityName =request.POST.get('myInput2')
    CharityiD=request.POST.get('myInput3')
    UserID=request.session['UserName']
    ob=Donor.objects.get(phone=UserID)
    user_data = {
        "RequestID":RequestID,
        "CharityName":CharityName,
        "CharityiD": CharityiD,
        "UserID":UserID,
        "UserNme":ob.Name,
      
        }
    return render(request,'donor/ViewAll3.html',user_data)
        


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


import datetime

@csrf_exempt

def ViewAll4(request):
    UserID=request.session['UserName']
    amount=request.GET.get("amt")
    RequestID=request.GET.get("Requestid")
    SENTERID=request.GET.get("SID")
    SENTERNAME=request.GET.get("SNAME")
    ReciverID=request.GET.get("RID")
    ReciverName=request.GET.get("RNAME")
    BillID=0;
    raised=0
    selected_rows = FinanceManagement.objects.filter(DetailsId=RequestID)
    for i in selected_rows:
        raised=raised+int(i.CrAmount)
    req=int((RequestDetailsTBL.objects.get(DetailsId=RequestID)).Amount)-raised

    current_datetime = datetime.datetime.now()

    if req<int(amount):
        data={"status":2,"msg":"You cannot pay this much amount. You can pay only "+str(req)+" amount or less "}
        return JsonResponse(data,safe=False)
    else:
        try:
            ob=FinanceManagement.objects.create(DetailsId=RequestID,FromID=SENTERID,ToID=ReciverID,CrAmount=amount,DataAndTime=current_datetime,Status=1) 
            BillID=ob.FinID




            filename = f"static/INVOICE{BillID}.pdf"  # Set the filename to match the request_id
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            doc = SimpleDocTemplate(response, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            heading = Paragraph("WebCharity", styles['Heading1'])
            heading = Paragraph("Payment Receipt", styles['Heading2'])
            story.append(heading)
            # Create paragraphs with the form data
            story.append(Paragraph(f"Date  : {current_datetime}", styles['Normal']))
            story.append(Paragraph(f"Payment ID  : {BillID}", styles['Normal']))
            story.append(Paragraph(f"Sender ID   : {SENTERID}", styles['Normal']))
            story.append(Paragraph(f"Sender Name : {SENTERNAME}", styles['Normal']))
            story.append(Paragraph(f"Receiver ID : {ReciverID}", styles['Normal']))
            story.append(Paragraph(f"Receiver Name : {ReciverName}", styles['Normal']))
            story.append(Paragraph(f"Amount: {amount}", styles['Normal']))

            # Build the PDF document
            doc.build(story)

           
            with open(filename, 'wb') as file_to_save:
                file_to_save.write(response.content)


            data={"status":1,"msg":" PAYMENT DONE "}
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            data={"status":3,"msg":" PAYMENT DONE "}
            return JsonResponse(data,safe=False)

@csrf_exempt

def myProfileDonor(request):
    phone_number = request.session['UserName']
    a=True
    if a:
        # Query the Donor model to fetch donor information by phone number
        ob = Donor.objects.get(phone=phone_number)
        
        # Pass the donor information to the template
        user = {
            'phone':ob.phone,
            'Name': ob.Name,
            'emaile': ob.email,
            'address': ob.address,
        
        }
        
        return render(request,'donor/myProfileDonor.html',user)
    else:
        
        return render(request, 'donor/myProfileDonor.html',{})    


@csrf_exempt
def ViewMyDonations(request):
    phone_number = request.session['UserName']
    data={}
    ob= FinanceManagement.objects.filter(FromID=phone_number)
    data1={}
    datalist=[]
    for i in ob:
        n=CharityRegistrationTBL.objects.get(phone=i.ToID)
        user_data = {
            "name": n.charityName,
            "date": i.DataAndTime,
            "amt": i.CrAmount,
            "TID": i.FinID,
            "PDF": "INVOICE"+str(i.FinID),
        }
        datalist.append(user_data)
    data["data"] = datalist   
    print(data) 
    return render(request,'donor/ViewMyDonations.html',data)


@csrf_exempt
def pdfDonerView(request):
    FIN=request.GET.get('FID')
    FIN="INVOICE"+str(FIN)+".pdf"
    print(FIN)
    return render(request,'donor/pdfDonerView.html',{"PDF":FIN})