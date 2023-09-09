from django.db import models
from django.contrib.auth.models import User
from staffpanel.models import learn_topic
from django.utils.timezone import now
# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    useremail = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    userrollno = models.CharField(max_length=50)
    usercontactto = models.CharField(max_length=50)
    msg = models.TextField()

    def __str__(self):
        return  self.username

class extra_info_of_bbsbec_user(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default='')
    user = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    gender = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=50,default='')
    intrest = models.CharField(max_length=50,default='')
    batch = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    crollno = models.CharField(max_length=50)
    urollno = models.CharField(max_length=50)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Blogcomment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(learn_topic,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:15]+'... By: '+str(self.user)
