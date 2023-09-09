import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from staffpanel.models import extra_info_of_professor, additional_info, add_chapter, learn_topic
from app.models import extra_info_of_bbsbec_user
from exam.models import studentquizzstatus
# Create your views here.


def index(request):
    return render(request, 'staffpanel/index.html')


def stafflogin(request):
    return render(request, 'staffpanel/login.html')


def handlestafflogin(request):
    if request.method == 'POST':
        staffuser = request.POST['suser']
        staffpassword = request.POST['spassword']
        auser = User.objects.filter(username=staffuser)
        if auser.count() != 0:
            auser = User.objects.get(username=staffuser)
            if auser.is_staff:
                auth_user = authenticate(
                    username=staffuser, password=staffpassword)
                if auth_user is not None:
                    auth_login(request, auth_user)
                    step2verification = extra_info_of_professor.objects.get(
                        user=staffuser)
                    if step2verification.step2verification == 'False':
                        messages.success(
                            request, "Logged in successfully Please Complete Second step of login by filling all the required fields")
                        return render(request, 'staffpanel/subjectaddition.html')
                    else:
                        messages.success(request, 'Logged in successfully')
                        return redirect('/staffpanel')
                else:
                    messages.error(request, "Invalid Credentials")
                    return redirect('/staffpanel/stafflogin')
            else:
                messages.error(
                    request, "Not Staff User Please login as student")
                return redirect('/app/userlogin')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/staffpanel/stafflogin')
    else:
        return redirect('/staffpanel/stafflogin')


def staffsignup(request):
    return render(request, 'staffpanel/signup.html')


def staffprofile(request):
    if request.user.is_staff:
        user=request.user
        user_basic_info = extra_info_of_professor.objects.filter(user=user)
        user_additional_info = additional_info.objects.filter(user=user)
        return render(request, 'staffpanel/staffprofile.html',{'userinfo':user_basic_info,'subjects':user_additional_info})
    else:
        return redirect('/staffpanel/stafflogin')

def handlestaffsignup(request):
    if request.method == "POST":
        Username = request.POST['user']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        # checking username exists
        checkemail = email.split('@')[1].lower()
        # if not checkemail == 'bbsbec.ac.in':
        #     messages.error(
        #         request, 'Please enter email id ending with "bbsbec.ac.in"')
        #     return redirect('/staffpanel/staffsignup')
        auser = User.objects.filter(username=Username)
        if auser.count() != 0:
            messages.error(request, "Username Already exists")
            return redirect('/staffpanel/staffsignup')
        aemail = User.objects.filter(email=email)
        if aemail.count() != 0:
            messages.error(request, "Email Already exists")
            return redirect('/staffpanel/staffsignup')
        # error checking
        if len(Username) > 20 or len(Username) < 5:
            messages.error(
                request, "Username must be between 5-10 letters/digits")
            return redirect('/staffpanel/staffsignup')
        if not Username.isalnum():
            messages.error(
                request, "Username Should not contain special charaters")
            return redirect('/staffpanel/staffsignup')
        if password != cpassword:
            messages.error(request, "Password Did not match")
            return redirect('/staffpanel/staffsignup')
        # user creation
        newuser = User.objects.create_user(Username, email, password)
        newuser.is_staff = True
        newuser.save()
        newuserextra = extra_info_of_professor(user=Username, name=name)
        newuserextra.save()
        auth_user = authenticate(username=Username, password=password)
        auth_login(request, auth_user)
        messages.success(request, "Please Fill additional information")
        return render(request, 'staffpanel/subjectaddition.html')
    else:
        return HttpResponse('404 Not found')


def subjectaddition(request):
    if request.method == 'POST' and request.user.is_staff:
        semester = request.POST['semester']
        group = request.POST['group']
        subject = request.POST['subject'].upper()
        user = request.user
        fetchdata = additional_info.objects.filter(
            user=user, semester=semester, group=group, subject=subject)
        if fetchdata.count() != 0:
            return HttpResponse("Subject Already exists")
        else:
            proname = extra_info_of_professor.objects.get(user=user)
            savedata = additional_info(
                user=user, semester=semester, group=group, subject=subject, name=proname.name)
            savedata.save()
            return HttpResponse('Added Successfully')
    else:
        return HttpResponse('Not Logged in or may not have sufficient permissions to perform this task')


def stafflogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "successfully logged out")
        return redirect('/staffpanel')
    else:
        return redirect('/staffpanel')


def displaycontent(request):
    if request.user.is_staff:
        return render(request, 'staffpanel/displaycontent.html')
    else:
        return redirect('/staffpanel/stafflogin')


def fetchsubjects(request):
    if request.method == 'POST':
        user = request.user
        newobj = additional_info.objects.filter(user=user)
        updates = []
        for item in newobj:
            updates.append({'semester': item.semester,
                            'group': item.group, 'subject': item.subject})
        response = json.dumps([updates], default=str)
        return HttpResponse(response)
    return redirect('/')


def chapters(request, slug):
    if request.user.is_staff:
        s = slug.split('-')
        sluggroup = s[0]
        slugsubject = s[1]
        return render(request, 'staffpanel/chapters.html', {'group': sluggroup, 'subject': slugsubject})
    else:
        return redirect('/staffpanel')


def chapteradd(request):
    if request.method == 'POST' and request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter'].upper()
        group = request.POST['group']
        user = request.user
        if len(chapter) < 4:
            return HttpResponse('failed')
        infocheck = add_chapter.objects.filter(
            user=user, chapter=chapter, group=group, subject=subject)
        if infocheck.count() != 0:
            return HttpResponse('chapter already exists')
        verifydata = additional_info.objects.filter(
            user=user, subject=subject, group=group)
        if verifydata.count() != 0:
            proname = extra_info_of_professor.objects.get(user=user)
            addnewchapter = add_chapter(
                user=user, chapter=chapter, group=group, subject=subject, name=proname.name)
            addnewchapter.save()
            return HttpResponse('Success')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse("failed")


def chapterfetcher(request):
    if request.method == 'POST' and request.user.is_staff:
        subject = request.POST['subject']
        group = request.POST['group']
        user = request.user
        newobj = add_chapter.objects.filter(
            user=user, subject=subject, group=group)
        if newobj.count() != 0:
            updates = []
            for item in newobj:
                updates.append({'chapter': item.chapter})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
        else:
            updates = []
            updates.append({'chapter': "Please add chapter"})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
    return redirect('/')


def topics(request, slug):
    try:
        if request.user.is_staff:
            x = slug.split("-")
            user = request.user
            group = x[0]
            subject = x[1]
            chapter = x[2]
            newobj = add_chapter.objects.filter(
                user=user, subject=subject, group=group)
            if newobj.count() != 0:
                return render(request, 'staffpanel/topicupdate.html', {'group': group, 'subject': subject, 'chapter': chapter})
            else:
                return redirect('/staffpanel')
        else:
            return redirect('/staffpanel')
    except Exception as e:
        return redirect('/staffpanel')


def topicdisplay(request):
    if request.user.is_staff:
        return render(request, 'staffpanel/topicupdate.html')
    else:
        return redirect('/staffpanel/stafflogin')


def topicadderdb(request):
    if request.method == 'POST' and request.user.is_staff:
        topicname = request.POST['topicname']
        if len(topicname) < 5:
            return HttpResponse('Error Not valid topic')
        videosource = request.POST['videosource']
        videolink = request.POST['videolink']
        topiccontent = request.POST['topiccontent']
        prismdisplay = request.POST['prismdisplay']
        group = request.POST['group']
        subject = request.POST['subject']
        sub_chapter = request.POST['chapter']
        announcement = request.POST['announcement']
        user = request.user
        newobj = add_chapter.objects.get(
            user=user, subject=subject, group=group, chapter=sub_chapter)
        if len(announcement) > 10:
            if newobj:
                newobj.topicname = topicname
                newobj.save()
                addtopic = learn_topic(user=user, subject=subject, group=group, topicname=topicname, videosource=videosource,
                                       videolink=videolink, topiccontent=topiccontent, prismdisplay=prismdisplay, chapter=sub_chapter, announcement=announcement)
                addtopic.save()
                return HttpResponse('s')
            else:
                return HttpResponse('Error Professor id mismatch')
        else:
            if newobj:
                newobj.topicname = topicname
                newobj.save()
                addtopic = learn_topic(user=user, subject=subject, group=group, topicname=topicname, videosource=videosource,
                                       videolink=videolink, topiccontent=topiccontent, prismdisplay=prismdisplay, chapter=sub_chapter)
                addtopic.save()
                return HttpResponse('s')
            else:
                return HttpResponse('Error Professor id mismatch')
    else:
        return HttpResponse('Error suspicious activity')


def step2verification(request):
    if request.method == 'POST' and request.user.is_staff:
        user = request.user
        fetchdata = additional_info.objects.filter(user=user)
        if fetchdata.count() != 0:
            updateprof = extra_info_of_professor.objects.get(user=user)
            updateprof.step2verification = 'True'
            updateprof.save()
            messages.success(request, 'Please continue with add topics and fetch students list professor verified')
            return redirect("/staffpanel")
        else:
            messages.error(
                request, 'Please add atleast one subject after login')
            return redirect('/staffpanel/stafflogin')


def topicfetcherdb(request):
    if request.method == 'POST' and request.user.is_staff:
        user = request.user
        group = request.POST['group']
        subject = request.POST['subject']
        sub_chapter = request.POST['chapter']
        newobj = learn_topic.objects.filter(
            user=user, group=group, subject=subject, chapter=sub_chapter)
        if newobj.count() != 0:
            updates = []
            for item in newobj:
                updates.append(
                    {'topic': item.topicname, 'source': item.videosource, 'time': item.timestamp})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
        else:
            updates = []
            updates.append({'topic': 'Error please add topics',
                            'source': 'System Admin Alert', 'time': 'Not Available'})
            response = json.dumps([updates], default=str)
            return HttpResponse(response)
    else:
        return redirect('/staffpanel')


def students(request,slug):
    if request.user.is_staff:
        group = slug
        user=request.user
        prof_finder=additional_info.objects.filter(group=group,user=user).count()
        if prof_finder !=0:
            userinfo = extra_info_of_bbsbec_user.objects.filter(group=group)
            return render(request, 'staffpanel/students.html',{'group':group,'students':userinfo})
        else:
            messages.error(request,'Slug Modification Detected you are not authorized to visit this group')
            return redirect('/staffpanel/displaycontent')
    else:
        messages.error(request,'Login with valid staff id required')
        return redirect('/staffpanel')       

def changepassword(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password != cpassword:
            messages.error(request,'Please Enter Correct Password')
            return redirect('/staffpanel/staffprofile')
        u = User.objects.get(username=user)
        u.set_password(password)
        u.save()
        messages.success(request,'Password Updated Successfully Login with new password')
        return redirect('/')
    else:
        return redirect('/')

# quizz add and display html page render
def displayquizz(request,slug):
    return render(request,'staffpanel/quizz.html',{'group':slug.split('-')[0],'subject':slug.split('-')[1],'chapter':slug.split('-')[2]})

#render add quizz page
def addquiz(request,slug):
    response = {'subject':slug.split('-')[0],'chapter':slug.split('-')[1],'group':slug.split('-')[2],'topic':slug.split('-')[3]}
    return render(request,'staffpanel/addquiz.html',response)

#display quizz result
def quizzresult(request, slug):
    subject = slug.split('-')[0]
    chapter = slug.split('-')[1]
    group = slug.split('-')[2]
    topic = slug.split('-')[3]
    fetchresult = studentquizzstatus.objects.filter(group=group,subject=subject,chapter=chapter,topic=topic)
    if fetchresult.count() != 0:
        quizzinfo = []
        for result in fetchresult:
            data = extra_info_of_bbsbec_user.objects.filter(user = result.username).first()
            quizzinfo.append({'marks':result.marks,'totalmarks':result.totalmarks,'uniroll':data.urollno,'name':data.name,'email':data.email})
    return render(request, 'staffpanel/quizzresult.html',{'students':quizzinfo,'group':group})