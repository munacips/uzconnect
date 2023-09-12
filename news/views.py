from django.shortcuts import render

from community.models import Account
from .models import Post, PostImage, PostComment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/community/login/')
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    context = {
        'posts' : posts
    }
    return render(request,'news/home.html',context)


@login_required(login_url='/community/login/')
def details(request,id):
    form = CommentForm(request.POST or None)
    post = Post.objects.get(id=id)
    post.views += 1
    post.save()
    pics = PostImage.objects.filter(post=post)
    comments = PostComment.objects.filter(post=post).order_by('-date_posted')
    if form.is_valid():
        comment = form.cleaned_data['comment']
        new_comment, created = PostComment.objects.get_or_create(post=post,author=request.user,comment=comment)
        new_comment.save()
        form = CommentForm()
    context = {
        'post' : post,
        'pics' : pics,
        'comments' : comments,
        'form' : form
    }
    return render(request,'news/details.html',context)