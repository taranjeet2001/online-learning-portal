from django.contrib import admin
from utils.models import Emailverify, basiccontact, Recorduserentry, Passwordreset,teacherimage
# Register your models here.
admin.site.register(Emailverify)
admin.site.register(basiccontact)
admin.site.register(Passwordreset)
admin.site.register(teacherimage)


@admin.register(Recorduserentry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip', ]
    list_filter = ['action', ]
