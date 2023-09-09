from django.urls import path
from utils import views


urlpatterns = [
    path('',views.index,name='home'),
    path('emailverify',views.emailverify,name='emailverify'),
    path('otpverify',views.otpverify,name='otpverify'),
    path('sendmail',views.sendmail,name='sendmail'),
    path('passwordreset',views.passwordreset,name='passwordreset'),
    path('uploadsystem',views.uploadsystem,name='uploadsystem'),
]