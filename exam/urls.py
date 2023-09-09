from django.urls import path
from exam import views


urlpatterns = [
    path('', views.index, name='home'),
    path('getquizz', views.quizzinfo, name='quizzinfo'),
    path('getquizzcontent', views.quizzdata, name='quizzdata'),
    path('quizzsubmit', views.quizzsubmit, name='quizzsubmit'),
    path('showquizz', views.showquizz, name='showquizz'),
    path('pushquizztopic', views.pushquizztopic, name='pushquizztopic'),
    path('addquestion', views.addquestion, name='addquestion'),
    path('displayquestions', views.displayquestions, name='displayquestions'),
    path('fetchquestion', views.fetchquestion, name='fetchquestion'),
    path('questionupdate', views.questionupdate, name='questionupdate'),
    path('deletequestion', views.deletequestion, name='deletequestion'),
]