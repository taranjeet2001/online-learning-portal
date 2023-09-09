from django.urls import path
from blog import views

urlpatterns = [
    path('',views.index,name='home'),
    path('posts/',views.posts,name='posts'),
    path('search/',views.search,name='search'),
    path('postcomment/',views.blogpostcomment,name='blogpostcomment'),
    path('article',views.article,name='article'),
    path('article/<str:slug>',views.article,name='article'),
]