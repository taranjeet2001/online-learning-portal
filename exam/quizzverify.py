from exam.models import Quizz
from exam.models import studentquizzstatus


def quizzchecking(request):
    data = request.POST
    group = request.user.first_name
    datalen = len(data)
    datalen = int((datalen-4)/3)
    subject = data['subject']
    chapter = data['chapter']
    topic = data['topic']
    totalmarks = 0
    marks = 0
    for i in range(datalen):
        I = i+1
        quizzdata = Quizz.objects.filter(subject=subject, topic=topic, chapter=chapter,
                                         group=group, question=data[f'question{I}'], answer=data[f'answer{I}']).first()
        totalmarks = totalmarks+int(data[f'marks{I}'])
        if quizzdata != None:
            marks = marks+int(data[f'marks{I}'])
        else:
            pass
    student_info = studentquizzstatus.objects.filter(
        username=request.user, group=group, subject=subject, chapter=chapter, topic=topic, totalmarks=totalmarks, status='done').count()
    if student_info == 0:
        studentinfo = studentquizzstatus(username=request.user, group=group, subject=subject,
                                         chapter=chapter, topic=topic, marks=marks, totalmarks=totalmarks, status='disabled')
        studentinfo.save()
