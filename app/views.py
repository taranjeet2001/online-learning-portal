import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from app.models import Contact, extra_info_of_bbsbec_user,Blogcomment
from staffpanel.models import additional_info, learn_topic, add_chapter
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from app.templatetags import get_dict
from utils.models import Passwordreset
from exam.models import studentquizzstatus
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    return render(request, 'app/index.html')

# user login page rendering
def userlogin(request):
    return render(request, 'app/login.html')


def usersignup(request):
    return render(request, 'app/signup.html')


def contact(request):
    if not request.user.is_authenticated:
        messages.error(
            request, 'You must be logged in before filling this form')
        return render(request, 'app/contactus.html', {'disabled': 'disabled'})
    else:
        return render(request, 'app/contactus.html', {'disabled': ''})


def contactform(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            name = request.POST.get('name')
            rollno = request.POST.get('rollno')
            requestto = request.POST.get('requestto')
            msg = request.POST.get('usermessage')
            clientkey = request.POST['g-recaptcha-response']
            secretkey = '6LdFKrMZAAAAAJr2CINLJHwR80kFCZcd_wdUxxZ9'
            captchaData = {
                'secret': secretkey,
                'response': clientkey
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=captchaData)
            response = json.loads(r.text)
            verify = response['success']
            if verify:
                contactsave = Contact(useremail=email, username=name,
                                      userrollno=rollno, usercontactto=requestto, msg=msg)
                contactsave.save()
                messages.success(request, 'Your request has been sent')
                return redirect('/app/contact')
            else:
                messages.error(
                    request, 'Sorry Rechaptcha Failed Please try again')
                return redirect('/app/contact')
        except Exception as e:
            print(e)
            messages.error(request, "Please submit correct information")
            return redirect('/app/contact')
    else:
        return redirect('/app')


def handlesignup(request):
    if request.method == "POST":
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6LdFKrMZAAAAAJr2CINLJHwR80kFCZcd_wdUxxZ9'
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        # r = requests.post(
        #     'https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        # response = json.loads(r.text)
        # verify = response['success']
        verify = True
        if verify:
            Username = request.POST.get('user', '')
            if len(Username) > 20 or len(Username) < 5:
                messages.error(
                    request, "Username must be between 5-10 letters/digits")
                return redirect('/app/usersignup')
            name = request.POST['name']
            email = request.POST['email'].lower()
            password = request.POST['pass']
            cpassword = request.POST['cpass']
            checkemail = email.split('@')[1].lower()
            if not checkemail == 'gmail.com':
                messages.error(
                    request, 'Please enter email id ending with "gmail.com"')
                return redirect('/app/usersignup')
            address = request.POST['address']
            state = request.POST['state']
            zipcode = request.POST['zip']
            batch = request.POST['year']
            group = request.POST['group']
            croll = request.POST['croll']
            uroll = request.POST['uroll']
            # checking username exists
            auser = User.objects.filter(username=Username)
            if auser.count() != 0:
                messages.error(request, "Username Already exists")
                return redirect('/app/usersignup')
            aemail = User.objects.filter(email=email)
            if aemail.count() != 0:
                messages.error(request, "Email Already exists")
                return redirect('/app/usersignup')
            # error checking
            if not Username.isalnum():
                messages.error(
                    request, "Username Should not contain special charaters")
                return redirect('/app/usersignup')
            if password != cpassword:
                messages.error(request, "Password Did not match")
                return redirect('/app/usersignup')
            # user creation
            newuser = User.objects.create_user(Username, email, password)
            newuser.first_name = group
            newuser.save()
            newuserextra = extra_info_of_bbsbec_user(
                user=Username, name=name, email=email, address=address, zipcode=zipcode, batch=batch, group=group, crollno=croll, urollno=uroll,state=state)
            newuserextra.save()
            messages.success(
                request, "User Created Successfully please login and start learning 'All the Best'")
            return redirect('/app/usersignup')
        else:
            messages.error(request, "Please verify Rechaptcha")
            return redirect('/app/usersignup')
    else:
        return redirect('/app')


def handlelogin(request):
    if request.method == "POST":
        luser = request.POST['luser']
        lpassword = request.POST['lpassword']
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6LdFKrMZAAAAAJr2CINLJHwR80kFCZcd_wdUxxZ9'
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        # r = requests.post(
        #     'https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        # response = json.loads(r.text)
        # verify = response['success']
        verify = True
        if verify:
            staff_check = User.objects.filter(username=luser)
            if staff_check.count() != 0:
                if staff_check[0].is_staff:
                    messages.error(request, "Please Login as staff")
                    return redirect('/staffpanel/stafflogin')
                auth_user = authenticate(username=luser, password=lpassword)
                if auth_user is not None:
                    auser = extra_info_of_bbsbec_user.objects.filter(
                        user=luser)
                    if auser.count() != 0:
                        auth_login(request, auth_user)
                        messages.success(request, "Logged in successfully")
                        return redirect('/app')
                else:
                    messages.error(
                        request, "Invalid Credentials,Please try again")
                    return redirect('/app/userlogin')
            else:
                messages.error(request, "Invalid Credentials,Please try again")
                return redirect('/app/userlogin')
        else:
            messages.error(request, "Please verify rechaptcha")
            return redirect('/app/userlogin')
    return redirect('/app/userlogin')


def handlelogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "successfully logged out")
        return redirect('/app')
    return redirect('/app')


def userprofile(request):
    if request.user.is_authenticated:
        auser = extra_info_of_bbsbec_user.objects.filter(user=request.user)
        if auser.count() != 0:
            return render(request, 'app/userprofile.html', {'userinfo': auser, 'bbsbecuser': True})
    else:
        return render(request, 'app/login.html')


# main class to learn topics
def classtopic(request, slug):
    if request.user.is_authenticated:
        renderdata = slug.split('-')
        subject = renderdata[0]
        chapter = renderdata[1]
        group = renderdata[2]
        topic = renderdata[3]
        newobj = learn_topic.objects.filter(
            subject=subject, group=group, chapter=chapter)
        if newobj.count() != 0:
            mainobj = learn_topic.objects.filter(
                subject=subject, group=group, chapter=chapter, topicname=topic).first()
            comments = Blogcomment.objects.filter(post=mainobj, parent=None)
            Replies = Blogcomment.objects.filter(
                post=mainobj).exclude(parent=None)
            repDict = {}
            for reply in Replies:
                if reply.parent.sno not in repDict.keys():
                    repDict[reply.parent.sno] = [reply]
                else:
                    repDict[reply.parent.sno].append(reply)
            context = {'objects': newobj, 'mainfile': mainobj,
                       'comments': comments, 'repDict': repDict}
            return render(request, 'app/class.html', context)
        else:
            messages.error(
                request, 'Prof have not added any topic to particular chapter')
            return redirect('/app')
    else:
        messages.error(request, 'You must login first')
        return redirect('/app/userlogin')

# fetching ajax info of subjects alloted to students


def fetchsubjects(request):
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        fetchuser = extra_info_of_bbsbec_user.objects.filter(user=user)
        group = fetchuser[0].group
        getsubjects = additional_info.objects.filter(group=group)
        if getsubjects.count() != 0:
            updates = []
            for item in getsubjects:
                updates.append(
                    {'subject': item.subject, 'group': item.group, 'name': item.name})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
        else:
            updates = []
            updates.append(
                {'subject': 'No subject', 'group': 'Please contact your respective prof to update subjects', 'name': 'not available'})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
    else:
        return redirect('/app/userlogin')

# page to display subjects to respective student


def learning(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return render(request, 'app/subjects.html')
    else:
        return redirect('/app/userlogin')
# page to display subjects ajax information


def chapters(request, slug):
    if request.user.is_authenticated:
        datarender = slug.split('-')
        subject = datarender[1]
        return render(request, 'app/chapters.html', {'subject': subject})
    return render(request, 'app/index.html')
# ajax availabel subjects to student


def chaptersdisplay(request):
    if request.user.is_authenticated and request.method == 'POST':
        subject = request.POST['subject']
        user = request.user
        userinfo = extra_info_of_bbsbec_user.objects.get(user=user)
        group = userinfo.group
        fetchchapters = add_chapter.objects.filter(
            group=group, subject=subject)
        if fetchchapters.count() != 0:
            updates = []
            for item in fetchchapters:
                updates.append(
                    {'chapter': item.chapter, 'time': item.timestamp, 'group': item.group, 'topic': item.topicname})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
        else:
            updates = []
            updates.append(
                {'chapter': 'No subject', 'time': 'Please contact your respective prof to update subjects', 'group': 'not available'})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
    else:
        return redirect('/app/userlogin')


def postcomment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = learn_topic.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        endurl = request.POST.get("urltoback")
        if parentSno == None:
            csave = Blogcomment(comment=comment, user=user, post=post)
            csave.save()
            messages.success(
                request, "your comment has been posted successfully")
        else:
            parent = Blogcomment.objects.get(sno=parentSno)
            csave = Blogcomment(comment=comment, user=user,
                                post=post, parent=parent)
            csave.save()
            messages.success(
                request, "your reply has been posted successfully")
        return redirect(endurl)
    else:
        return redirect('/app/')


def passwordreset(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        url = request.POST['urltoback']
        checkotp = Passwordreset.objects.filter(email=email, otp=otp).count()
        if password != cpassword:
            messages.error(request,'Password Mismatch please try again')
            return redirect('/app/userlogin')
        if checkotp != 0:
            u = User.objects.get(email=email)
            u.set_password(password)
            u.save()
            messages.success(request,'Password Changed Successfully please signin with new password')
            return redirect(url)
    else:
        return redirect('/app/')

# quizz page rendering
def quizztest(request,slug):
    subject = slug.split('-')[0]
    chapter = slug.split('-')[1]
    return render(request,'app/quizz.html',{'subject':subject,'chapter':chapter})

# display results for students
def result(request):
    user = request.user
    results = studentquizzstatus.objects.filter(username=user)
    paginator = Paginator(results, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'app/result.html',{'results':page_obj})