from django.contrib import admin
from blog.models import Post,Postcomment
# Register your models here.
admin.site.register(Postcomment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('blog/tiny.js',)
