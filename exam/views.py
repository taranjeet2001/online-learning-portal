from django.contrib import messages
from exam.quizzverify import quizzchecking
from django.shortcuts import redirect, render, HttpResponse
from exam.models import Quizz, Quizztopic, studentquizzstatus
from exam.quizzverify import quizzchecking
import json
# Create your views here.


def index(request):
    return render(request, 'exam/index.html')

# to display quizz available for group+student+subject+chapter


def quizzinfo(request):
    if request.method == "POST" and request.user.is_authenticated and not request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        group = request.user.first_name
        available_quizzs = Quizztopic.objects.filter(
            subject=subject, chapter=chapter, group=group)
        if available_quizzs.count() != 0:
            quizzlist = []
            for item in available_quizzs:
                fetchdata = studentquizzstatus.objects.filter(
                    subject=subject, group=group, chapter=chapter, topic=item.topic, username=request.user).first()
                if fetchdata != None:
                    quizzlist.append({'time': item.date, 'topic': item.topic,
                                      'status': fetchdata.status, 'statusmessage': 'Done'})
                else:
                    quizzlist.append(
                        {'time': item.date, 'topic': item.topic, 'status': '', 'statusmessage': 'Start'})
            response = json.dumps([quizzlist], default=str)
            return HttpResponse(response)
        else:
            errors = []
            errors.append(
                {'time': "0000-00-00", 'topic': 'no topic'})
            response = json.dumps([errors], default=str)
            return HttpResponse(response)
    else:
        return HttpResponse('not a user')

# to display content to quizz q/n


def quizzdata(request):
    if request.method == "POST" and request.user.is_authenticated and not request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        topic = request.POST['topic']
        group = request.user.first_name
        available_quizzs = Quizz.objects.filter(
            subject=subject, chapter=chapter, group=group, topic=topic).exclude(status='draft')
        if available_quizzs.count() != 0:
            quizzlist = []
            for item in available_quizzs:
                quizzlist.append(
                    {'time': item.date, 'topic': item.topic, 'question': item.question, 'option1': item.option1, 'option2': item.option2, 'option3': item.option3, 'option4': item.option4 , 'marks':item.marks})
            response = json.dumps([quizzlist], default=str)
            return HttpResponse(response)
        else:
            errors = []
            errors.append({})
            response = json.dumps([errors], default=str)
            return HttpResponse(response)
    else:
        return HttpResponse('not a student user')

# accepting quizz from user


def quizzsubmit(request):
    if request.method == 'POST' and request.user.is_authenticated and not request.user.is_staff:
        response = quizzchecking(request)
        url = request.POST['urltoback']
        messages.success(request,'Quizz submitted successfully please check result in profile section')
        return redirect(url)
    else:
        return redirect('/')

# rendering quizz tooics to prof


def showquizz(request):
    if request.method == 'POST' and request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        group = request.POST['group']
        available_quizzs = Quizztopic.objects.filter(
            subject=subject, chapter=chapter, group=group)
        if available_quizzs.count() != 0:
            quizzlist = []
            for item in available_quizzs:
                fetchdata = studentquizzstatus.objects.filter(
                    subject=subject, group=group, chapter=chapter, topic=item.topic, username=request.user).first()
                if fetchdata != None:
                    quizzlist.append({'time': item.date, 'topic': item.topic,
                                      'status': fetchdata.status, 'statusmessage': 'Done'})
                else:
                    quizzlist.append(
                        {'time': item.date, 'topic': item.topic, 'status': '', 'statusmessage': 'Start'})
            response = json.dumps([quizzlist], default=str)
            return HttpResponse(response)
        else:
            errors = []
            errors.append(
                {'time': "0000-00-00", 'topic': 'no topic'})
            response = json.dumps([errors], default=str)
            return HttpResponse(response)

# add quizz topics to database
def pushquizztopic(request):
    if request.method == 'POST' and request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        group = request.POST['group']
        topic = request.POST['topic'].upper()
        if len(topic) > 5:
            adddata = Quizztopic(
                subject=subject, chapter=chapter, group=group, topic=topic)
            adddata.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failed')

#add quizz questions to database
def addquestion(request):
    if request.method == 'POST' and request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        group = request.POST['group']
        topic = request.POST['topic']
        currectoption = request.POST['answer']
        answer = request.POST[currectoption]
        question = request.POST['question']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        marks = int(request.POST['marks'])
        if len(question) < 5 and len(option1) < 1 and len(option2) < 1 and len(option3) < 1 and len(option4) < 1:
            return HttpResponse('Error')
        adddata = Quizz(subject=subject, topic=topic, chapter=chapter, group=group, question=question, option1=option1,
                        option2=option2, option3=option3, option4=option4, marks=marks, answer=answer, status='published')
        adddata.save()
        return HttpResponse('success')
    else:
        return HttpResponse('Error')

#display questions to professors
def displayquestions(request):
    if request.method == 'POST' and request.user.is_staff:
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        group = request.POST['group']
        topic = request.POST['topic']
        fetchquestions = Quizz.objects.filter(subject=subject,chapter=chapter,topic=topic,group=group)
        if fetchquestions.count() != 0:
            quizzlist = []
            for item in fetchquestions:
                quizzlist.append({'sno': item.sno, 'question': item.question})
            response = json.dumps([quizzlist], default=str)
            return HttpResponse(response)
        else:
            errors = []
            errors.append(
                {'sno': 'nothing', 'question': "missing"})
            response = json.dumps([errors], default=str)
            return HttpResponse(response)
    else:
        return HttpResponse('hello')

#display question for edit
def fetchquestion(request):
    if request.method == 'POST' and request.user.is_staff:
        sno = int(request.POST['sno'])
        item = Quizz.objects.filter(sno=sno).first()
        quizzlist = []
        quizzlist.append({'question': item.question, 'option1': item.option1, 'option2': item.option2, 'option3': item.option3, 'option4': item.option4,'marks':item.marks,'answer':item.answer})
        response = json.dumps([quizzlist], default=str)
        return HttpResponse(response)
    else:
        return HttpResponse('error')

#updating question as per prof request
def questionupdate(request):
    if request.method == 'POST' and request.user.is_staff:
        sno = request.POST['sno']
        currectoption = request.POST['Currectoption']
        answer = request.POST[currectoption]
        question = request.POST['Question']
        option1 = request.POST['Option1']
        option2 = request.POST['Option2']
        option3 = request.POST['Option3']
        option4 = request.POST['Option4']
        url= request.POST['urltoback']
        marks = int(request.POST['Marks'])
        if len(question) < 5 and len(option1) < 1 and len(option2) < 1 and len(option3) < 1 and len(option4) < 1:
            messages.error(request,'Please make correct question')
            return redirect(url)
        searchquestion = Quizz.objects.filter(sno=sno).first()
        searchquestion.question=question
        searchquestion.option1=option1
        searchquestion.option2=option2
        searchquestion.option3=option3
        searchquestion.option4=option4
        searchquestion.marks=marks
        searchquestion.answer=answer
        searchquestion.save()
        messages.success(request,'Question Updated')
        return redirect(url)
    else:
        return redirect('/')
#delete a question of prof request
def deletequestion(request):
    if request.method == 'POST' and request.user.is_staff:
        sno = request.POST['sno']
        url = request.POST['urltoback']
        Quizz.objects.filter(sno=sno).delete()
        messages.success(request,'Question Deleted')
        return HttpResponse('success')
    else:
        messages.error(request,'UnAuthorized')
        return redirect('/')