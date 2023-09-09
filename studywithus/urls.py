"""studywithus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from studywithus import views
from django.contrib import admin
from django.conf.urls import url

# easy admin modify method
admin.site.site_title = "Learn from professionals in better way"
admin.site.site_header = "Learn Skills"
admin.site.index_title = "Welcome to learn skills admin panel"

handler404 = 'studywithus.views.page_not_found_view'
handler500 = 'studywithus.views.server_error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('contactform', views.contactform, name='contactform'),
    path('sitemap.xml', views.sitemaper, name='sitemaper'),
    path('app/', include('app.urls')),
    path('staffpanel/', include('staffpanel.urls')),
    path('utils/', include('utils.urls')),
    path('blog/', include('blog.urls')),
    path('exam/', include('exam.urls')),
    url(r'^robots\.txt', include('robots.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
