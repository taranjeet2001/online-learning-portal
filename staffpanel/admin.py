from django.contrib import admin
from staffpanel.models import extra_info_of_professor,additional_info,add_chapter,learn_topic
# # Register your models here.
admin.site.register(extra_info_of_professor)
admin.site.register(additional_info)
admin.site.register(add_chapter)
admin.site.register(learn_topic)