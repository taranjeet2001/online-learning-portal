import random
from django.shortcuts import render, redirect, HttpResponse
from blog.models import Post, Postcomment
from django.http import Http404
from blog.templatetags import get_dict
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    articles = list(Post.objects.all().exclude(status='draft'))
    articles_len = Post.objects.all().count()
    if articles_len < 6:
        pass
    else:
        articles = random.sample(articles, 6)
    return render(request, 'blog/index.html', {'articles': articles})


def article(request, slug):
    post = Post.objects.filter(slug=slug).exclude(status='draft').first()
    comments = Postcomment.objects.filter(post=post, parent=None)
    Replies = Postcomment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in Replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] =[reply]
        else:
            repDict[reply.parent.sno].append(reply)
    if post != None:
        context = {'article': post, 'comments': comments,'repDict':repDict}
        return render(request,'blog/article.html',context)
    else:
        raise Http404()


def posts(request):
    articles = list(Post.objects.all().exclude(status='draft'))
    paginator = Paginator(articles, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/posts.html', {'articles': page_obj})


def search(request):
    query = request.GET['search']
    checker = True
    mcat = Post.objects.filter(
        category__icontains=query).exclude(status='draft')
    mtitle = Post.objects.filter(
        title__icontains=query).exclude(status='draft')
    m_title_cat = mcat.union(mtitle)
    mcontent = Post.objects.filter(
        content__icontains=query).exclude(status='draft')
    m_title_cat_content = mcontent.union(m_title_cat)
    if m_title_cat_content.count() == 0:
        checker = False
    return render(request, 'blog/search.html', {'articles': m_title_cat_content, "query": query, 'checker': checker})


def blogpostcomment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == None:
            csave = Postcomment(comment=comment, user=user, post=post)
            csave.save()
            messages.success(
                request, "your comment has been posted successfully")
        else:
            parent = Postcomment.objects.get(sno=parentSno)
            csave = Postcomment(comment=comment, user=user,
                                post=post, parent=parent)
            csave.save()
            messages.success(
                request, "your reply has been posted successfully")
    return redirect(f'/blog/article/{post.slug}')
