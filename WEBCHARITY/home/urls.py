from django.urls import path
from . import views
urlpatterns = [

# home 

path('site/',views.Index,name='site'),
path('login/',views.Login,name='login'),
path('CheckLogin/',views.CheckLogin,name='CheckLogin'),
path('adminhome/',views.adminhome,name='adminhome'),
path('charityhome/',views.charityhome,name='charityhome'),
path('donorhome/',views.donorhome,name='donorhome'),
path('CharityReg/',views.CharityReg,name='CharityReg'),
path('RegCharity/',views.RegCharity,name='RegCharity'),
path('DonorReg/',views.DonorReg,name='DonorReg'),
path('RegDonor/',views.RegDonor,name='RegDonor'),
path('about/',views.about,name='about'),
path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
path('forgotPassword2/',views.forgotPassword2,name='forgotPassword2'),

# admin

path('ViewUser/',views.ViewUser,name='ViewUser'),
path('ViewUser2/',views.ViewUser2,name='ViewUser2'),
path('ApproveCharity/',views.ApproveCharity,name='ApproveCharity'),
path('ApproveCharity2/',views.ApproveCharity2,name='ApproveCharity2'),
path('ApproveCharity3/',views.ApproveCharity3,name='ApproveCharity3'),
path('ApproveDonation/',views.ApproveDonation,name='ApproveDonation'),
path('ApproveDonation2/',views.ApproveDonation2,name='ApproveDonation2'),
path('ApproveDonation3/',views.ApproveDonation3,name='ApproveDonation3'),
path('pdfDonationViewAdmin/',views.pdfDonationViewAdmin,name='pdfDonationViewAdmin'),
path('viewcharities/',views.viewcharities,name='viewcharities'),
path('viewcharities2/',views.viewcharities2,name='viewcharities2'),
path('DonationStatusAdmin/',views.DonationStatusAdmin,name='DonationStatusAdmin'),
path('DonationStatusAdmin2/',views.DonationStatusAdmin2,name='DonationStatusAdmin2'),




#charity
path('DonationRequesthtml/',views.DonationRequesthtml,name='DonationRequesthtml'),
path('DonationRequest/',views.DonationRequest,name='DonationRequest'),
path('MyProfileCharity/',views.MyProfileCharity,name='MyProfileCharity'),
path('pdfDonationViewCharity/',views.pdfDonationViewCharity,name='pdfDonationViewCharity'),
path('RequetStatusCharity/',views.RequetStatusCharity,name='RequetStatusCharity'),
path('RequetStatusCharity2/',views.RequetStatusCharity2,name='RequetStatusCharity2'),





#Donor
path('ViewAll/',views.ViewAll,name='ViewAll'),
path('ViewAll2/',views.ViewAll2,name='ViewAll2'),
path('ViewAll3/',views.ViewAll3,name='ViewAll3'),
path('ViewAll4/',views.ViewAll4,name='ViewAll4'),
path('ViewMyDonations/',views.ViewMyDonations,name='ViewMyDonations'),
path('myProfileDonor/',views.myProfileDonor,name='myProfileDonor'),
path('pdfDonerView/',views.pdfDonerView,name='pdfDonerView'),

]
