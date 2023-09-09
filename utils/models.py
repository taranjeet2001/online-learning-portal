from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
# Create your models here.


class Emailverify(models.Model):
    sno = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class basiccontact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Emaildataofuser(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    rollno = models.CharField(max_length=50)
    profname = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# login logout failed with ip address record saving


class Recorduserentry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Recorduserentry.objects.create(
        action='user_logged_in', ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Recorduserentry.objects.create(
        action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    Recorduserentry.objects.create(
        action='user_login_failed', username=credentials.get('username', None))


class Passwordreset(models.Model):
    sno = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254)
    otp = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class teacherimage(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to='teachers/questions', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.username
