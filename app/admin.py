from django.contrib import admin
from app.models import Contact,extra_info_of_bbsbec_user,Blogcomment
# Register your models here.

admin.site.register(Contact)
admin.site.register(extra_info_of_bbsbec_user)
admin.site.register(Blogcomment)