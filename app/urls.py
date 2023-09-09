from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='home'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('postcomment', views.postcomment, name='postcomment'),
    path('usersignup', views.usersignup, name='usersignup'),
    path('contact', views.contact, name='contact'),
    path('contactform', views.contactform, name='contactform'),
    path('signup', views.handlesignup, name='handlesignup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('learning', views.learning, name='learning'),
    path('chapters', views.chapters, name='chapters'),
    path('chapters/<str:slug>', views.chapters, name='chapters'),
    path('chaptersdisplay', views.chaptersdisplay, name='chaptersdisplay'),
    path('class', views.classtopic, name='classtopic'),
    path('class/<str:slug>', views.classtopic, name='classtopic'),
    path('fetchsubjects', views.fetchsubjects, name='fetchsubjects'),
    path('passwordreset', views.passwordreset, name='passwordreset'),
    path('quizz', views.quizztest, name='quizztest'),
    path('quizz/<str:slug>', views.quizztest, name='quizztest'),
    path('results', views.result, name='result'),
]
