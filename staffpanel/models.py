from django.db import models
from staffpanel.fields import NonStrippingTextField
from django.utils.timezone import now
# Create your models here.


class extra_info_of_professor(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    step2verification = models.CharField(max_length=50, default="False")
    subjects = models.CharField(max_length=500)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class additional_info(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    user = models.CharField(max_length=50, default='lucifer')
    semester = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)

    def __str__(self):
        return self.user


class add_chapter(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50,default='')
    chapter = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    topicname = models.CharField(max_length=100,default='')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.user


class learn_topic(models.Model):
    sno=models.AutoField(primary_key=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    chapter = models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    topicname = models.CharField(max_length=100, blank=True, null=True)
    videosource = models.CharField(max_length=10, blank=True, null=True)
    videolink = models.URLField(max_length=200, blank=True, null=True)
    topiccontent = models.TextField(blank=True, null=True)
    prismdisplay = NonStrippingTextField(default='', blank=True, null=True)
    timestamp = models.DateTimeField(default=now)
    updatetimestamp = models.DateTimeField(auto_now=True)
    announcement = models.CharField(max_length=100,default='Any Course related announcements will be posted here')

    def __str__(self):
        return self.user
