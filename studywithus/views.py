from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import requests
import json
from utils.models import basiccontact
# sitemap display with modifications
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import StaticSitemap
from app.sitemaps import studentStaticSitemap
# sitemap stuff
from functools import wraps
from django.utils.http import http_date
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site
import datetime
from calendar import timegm
from django.template.response import TemplateResponse
def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def contactform(request):
    if request.method == 'POST':
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6LdFKrMZAAAAAJr2CINLJHwR80kFCZcd_wdUxxZ9'
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']
        if verify:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            message = request.POST['message']
            datasave = basiccontact(
                name=name, email=email, phone=phone, message=message)
            datasave.save()
            messages.success(request, 'Contact Submitted Successfully')
            return redirect('/contact')
        else:
            messages.error(request, 'Please verify rechaptcha')
            return redirect('/contact')
    else:
        pass

# sitemap modified function to design it in better way
@x_robots_tag
def sitemaper(request,section=None,template_name='sitemap.xml',content_type='application/xml'):
    sitemaps = {
        'static': StaticSitemap(),
        'studentstatic': studentStaticSitemap()
    }
    req_protocol = request.scheme
    req_site = get_current_site(request)
    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)

    lastmod = None
    all_sites_lastmod = True
    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
            if all_sites_lastmod:
                site_lastmod = getattr(site, 'latest_lastmod', None)
                if site_lastmod is not None:
                    site_lastmod = (
                        site_lastmod.utctimetuple() if isinstance(site_lastmod, datetime.datetime)
                        else site_lastmod.timetuple()
                    )
                    lastmod = site_lastmod if lastmod is None else max(lastmod, site_lastmod)
                else:
                    all_sites_lastmod = False
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},content_type=content_type)
    if all_sites_lastmod and lastmod is not None:
        # if lastmod is defined for all sites, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(timegm(lastmod))
    return response

def page_not_found_view(request,exception):
    return render(request,'404.html')

def server_error_view(request):
    return render(request,'500.html')