from django.db import models
from django.utils.timezone import now
# Create your models here.

STATUS = (
    ('draft', 'draft'),
    ('published', 'published'),
)
STUDENT_QUIZZ_STATUS = (
    ('disabled', 'done'),
    ('pending', 'pending'),
)


class Quizztopic(models.Model):
    sno = models.AutoField(primary_key=True)
    group = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    chapter = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=now)
    date = models.DateField(default=now)

    def __str__(self):
        return self.topic


class Quizz(models.Model):
    sno = models.AutoField(primary_key=True)
    group = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    chapter = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=now)
    date = models.DateField(default=now)
    marks =models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')

    def __str__(self):
        return self.subject


class studentquizzstatus(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    group = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    chapter = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    marks = models.IntegerField()
    totalmarks = models.IntegerField()
    status = models.CharField(max_length=20, choices=STUDENT_QUIZZ_STATUS, default='pending')

    def __str__(self):
        return self.username
