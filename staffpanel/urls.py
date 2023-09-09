from django.urls import path
from staffpanel import views

urlpatterns = [
    path('',views.index,name='home'),
    path('stafflogin',views.stafflogin,name='stafflogin'),
    path('stafflogout',views.stafflogout,name='stafflogout'),
    path('staffsignup',views.staffsignup,name='staffsignup'),
    path('handlestafflogin',views.handlestafflogin,name='handlestafflogin'),
    path('staffprofile',views.staffprofile,name='staffprofile'),
    path('handlestaffsignup',views.handlestaffsignup,name='handlestaffsignup'),
    path('subjectaddition',views.subjectaddition,name='subjectaddition'),
    path('displaycontent',views.displaycontent,name='displaycontent'),
    path('fetchsubjects',views.fetchsubjects,name='fetchsubjects'),
    path('addchapter',views.chapteradd,name='chapteradd'),
    path('chapterfetcher',views.chapterfetcher,name='chapterfetcher'),
    path('chaptertopic',views.topicdisplay,name='topicdisplay'),
    path('topicadderdb',views.topicadderdb,name='topicadderdb'),
    path('step2verification',views.step2verification,name='step2verification'),
    path('topicfetcherdb',views.topicfetcherdb,name='topicfetcherdb'),
    path('topics/<str:slug>',views.topics,name='topics'),
    path('chapters/<str:slug>',views.chapters,name='chapters'),
    path('students/<str:slug>',views.students,name='students'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('quizz/<str:slug>',views.displayquizz,name='displayquizz'),
    path('addquiz/<str:slug>',views.addquiz,name='addquiz'),
    path('quizzresult/<str:slug>',views.quizzresult,name='quizzresult'),
]
