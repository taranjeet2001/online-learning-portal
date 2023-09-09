from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils.timezone import now

from blog.sluggeneration import unique_slug_generator

# Create your models here.
STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)
CATEGORY_CHOICES = (
    ('Hacking', 'Hacking'),
    ('C++', 'C++'),
)
AUTHOR_CHOICES = (
    ('Gurjeet S Grewal', 'Gurjeet S Grewal'),
)
PDFSOURCE_CHOICES = (
    ('Google', 'Google'),
    ('Media', 'Media'),
)


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    keyword = models.CharField(max_length=100)
    description = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    author = models.CharField(
        max_length=20, choices=AUTHOR_CHOICES, default='Gurjeet S Grewal')
    pdffile_source = models.CharField(
        max_length=20, choices=PDFSOURCE_CHOICES, default='Google')
    pdffile = models.FileField(upload_to='blog/posts/pdfs', blank=True)
    pdflink = models.URLField(max_length=300, blank=True)
    shortdesc = models.CharField(max_length=150, default='')
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='Hacking')
    image = models.ImageField(
        upload_to='blog/posts', height_field=None, width_field=None, max_length=None)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title


def slug_generator(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)


class Postcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:15]+'... By: '+str(self.user)
        


