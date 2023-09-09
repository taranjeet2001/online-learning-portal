from django.shortcuts import render, redirect
from django.http import HttpResponse
import math
import random
# for email
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
# for getting templates from templates folder
# from django.template.loader import render_to_string
# modules for email sending
# import smtplib
# from email.message import EmailMessage
# from string import Template
# import string
# from smtplib import SMTP
# import os
# import sys
from django.contrib import messages
from utils.models import Emailverify, Emaildataofuser, Passwordreset, teacherimage
from validate_email import validate_email
from django.contrib.auth.models import User
from image_optimizer.utils import image_optimizer
# custom functions
# from django.contrib.sites.models import Site


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

# Create your views here.
# def siteidget():
#     id = Site.objects.get_current()
#     return id


def index(request):
    # sitename = input('Enter Site Name')
    # addsite = Site.objects.create(domain=sitename, name=sitename)
    # addsite.save()
    return redirect('/')


def emailverify(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        auser = User.objects.filter(email=email)
        if auser.count() != 0:
            return HttpResponse("Error Email already exists")
        # is_valid = validate_email(email_address=email, check_mx=True, from_address='bbsbecteam@upatmastaff.com', helo_host='upatmastaff.com', smtp_timeout=10, dns_timeout=10, use_blacklist=True, debug=False)
        is_valid = True
        otp = generateOTP()
        if is_valid:
            try:
                checkemail = Emailverify.objects.filter(email=email).first()
                if checkemail != None:
                    checkemail.otp = otp
                    checkemail.save()
                    emailsending(email, 'Otp Verification for new user',
                                 f'Your Otp for Registration is {otp}')
                    return HttpResponse(f'Otp has been sent successfully to {email}')
                else:
                    saveotp = Emailverify(email=email, otp=otp)
                    saveotp.save()
                    emailsending(email, 'Otp Verification for new user',
                                 f'Your Otp for Registration is {otp}')
                    return HttpResponse(f'otp sent successfully to {email}')
            except Exception as e:
                print(e)
                return HttpResponse('Error otp not sent please check mail id')
        else:
            return HttpResponse('Error Please use proper email address')
    else:
        return redirect('/')


def otpverify(request):
    if request.method == 'POST':
        email = request.POST['email']
        verifyotp = request.POST['otp']
        checkemail = Emailverify.objects.get(email=email)
        if checkemail.otp == verifyotp:
            return HttpResponse('Email verified successfully')
        else:
            return HttpResponse('Error Please check otp')
    else:
        return redirect('/')


def sendmail(request):
    if request.method == 'POST' and request.user.is_staff:
        sname = request.POST['sname']
        email = request.POST['email']
        rollno = request.POST['rollno']
        profname = request.POST['profname']
        subject = request.POST['subject']
        message = request.POST['message']
        urltoback = request.POST['urltoback']
        datasave = Emaildataofuser(
            name=sname, email=email, rollno=rollno, profname=profname, subject=subject, message=message)
        datasave.save()
        try:
            text_body = f'Prof name: {profname} message is: {message}'
            emailsending(email, subject, text_body)
            messages.success(request, f'Mail is sent to student: {sname}')
            return redirect(urltoback)
        except Exception as e:
            messages.error(request, 'Error occured sending mail')
            return redirect(urltoback)


def passwordreset(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        emailcheck = User.objects.filter(email=email).count()
        if emailcheck != 0:
            otp = generateOTP()
            emailsending(email, 'Password Reset LearnSkills',
                         f'Your Otp for password reset is {otp}')
            datasave = Passwordreset(email=email, otp=otp)
            datasave.save()
            return HttpResponse('Otp Sent Successfully please check mailbox/spambox')
        else:
            return HttpResponse('Error User does not exists')
    else:
        return redirect('/app/userlogin/')


def emailsending(email, subject, message):
    msg = EmailMultiAlternatives(
        subject=subject, from_email="admin@sampurnanagar.com", to=[email], body=message)
    msg.send()
    return 0


def uploadsystem(request):
    if request.method == 'POST' and request.user.is_staff:
        username = request.user
        image = request.FILES['image']
        if image.size > 5242880:
            return HttpResponse('Error File size large then 5 MB')
        elif image.size < 1024:
            return HttpResponse('Error File size smaller then 1 KB')
        else:
            image = image_optimizer(image_data=image,output_size=(800, 800),resize_method='cover')
            savedata = teacherimage(username=username, image=image)
            savedata.save()
            return HttpResponse('File Uploaded please select from folder to use it')
    elif request.user.is_staff:
        fetchimage = teacherimage.objects.filter(username=request.user)
        return render(request, 'utils/test.html',{'images':fetchimage})
    else:
        return redirect('/')

