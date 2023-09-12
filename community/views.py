from django.http import HttpResponse
from django.shortcuts import render, redirect
from news.models import Post, PostImage
from .models import Quote, Account, QuoteLike, Comment
from .forms import CommentForm, ConfirmEmail, ProgramForm, SearchUserForm, LoginForm, SignUpForm, QuoteForm, ArticleForm, AddPicsForms, GoodForm, ServiceForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from news.views import home as main
from news.views import details
from biz.models import Good, Service
from django.conf import settings
from django.core.mail import send_mail
import random


@login_required(login_url='/community/login/')
def home(request):
    form = QuoteForm(request.POST or None)
    user = request.user
    acc = Account.objects.get(user=user)
    following = acc.following.all()
    posts = Quote.objects.none()
    recos = Quote.objects.none()
    for i in following:
        posts |= Quote.objects.filter(quoter=i)
    posts = posts.order_by('-time')
    if form.is_valid():
        post = form.cleaned_data['quote']
        new_quote,created = Quote.objects.get_or_create(quoter=request.user,quote=post)
        new_quote.save()
        form = QuoteForm()
        context = {
            'posts' : posts,
            'acc' : acc,
            'form' : form
        }
        return render(request,'community/home.html',context)
    context = {
        'posts' : posts,
        'acc' : acc,
        'form' : form
    }
    return render(request,'community/home.html',context)


@login_required(login_url='/community/login/')
def coursemash(request):
    form = ProgramForm(request.POST or None)
    if form.is_valid():
        query = form.cleaned_data['program']
        accs = Account.objects.filter(program=query)
        context = {
            'accs' : accs,
            'form' : form,
        }
        return render(request,'community/coursemash.html',context)
    context = {
        'form' : form,
    }
    return render(request,'community/coursemash.html',context)


@login_required(login_url='/community/login/')
def studentsearch(request):
    form = SearchUserForm(request.POST or None)
    acc = Account.objects.get(user=request.user)
    if form.is_valid():
        query = form.cleaned_data['name']
        users = User.objects.filter(username__icontains=query)
        users |= User.objects.filter(first_name__icontains=query)
        users |= User.objects.filter(last_name__icontains=query)
        context = {
            'users' : users,
            'form' : form,
            'acc' : acc,
        }
        return render(request,'community/studentsearch.html',context)
    context = {
        'form' : form,
    }
    return render(request,'community/studentsearch.html',context)


def log_in(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            if Account.objects.get(user=user).activated:
                login(request , user)
                return redirect(request.GET.get('next'))
    else:
        return render(request,'community/login.html',context = {
            'text':'Wrong details',
            'form': form
            })
    
    context ={
        'form' : form
    }
    return render(request,'community/login.html', context)


@login_required(login_url='/community/login/')
def log_out(request):
    logout(request)
    return log_in(request)


def signup(request):
    form = SignUpForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        #new_user = form.save(commit = False)
        username = form.cleaned_data['username']
        password = make_password(form.cleaned_data['password'])
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        program = form.cleaned_data['program']
        if form.cleaned_data['display_picture']:
            dp = request.FILES['display_picture']
        integer = random.randint(100000,999999)
        ##dp_id = disp_pic.id
        #userlist = [integer,username,password,first_name,last_name,email,program,dp_id]
        new_user , created = User.objects.get_or_create(username=username,first_name=first_name,password=password,last_name=last_name,email=email,)
        new_acc , created = Account.objects.get_or_create(user=new_user,program=program,display_picture=dp)
        send_mail(
            "Confirmation Email",#subject
            f'This is your confirmation number {integer}',#message
            settings.EMAIL_HOST_USER,#from email
            [email],#sendt0
            fail_silently=False,
        )
        data = [integer,new_acc.id]
        request.session['data'] = data
        return redirect('/community/confirm/') #confirm(request,integer,username,first_name,password,last_name,email,program,dp)
    context = {
        'form' :  form
    }
    return render(request , 'community/signup.html' , context)


@login_required(login_url='/community/login/')
def account(request):
    user = request.user
    acc = Account.objects.get(user=user)
    quotes = Quote.objects.filter(quoter=request.user)
    goods = Good.objects.filter(provider=acc)
    services = Service.objects.filter(provider=acc)
    context = {
        'acc' : acc,
        'quotes' : quotes,
        'goods' : goods,
        'sers' : services
    }
    return render(request,'community/myaccount.html',context)


@login_required(login_url='/community/login/')
def myprofile(request):
    if isinstance(request.user, User):
        id = request.user.id
    user = User.objects.get(id=id)
    acc = Account.objects.get(user=user)
    context = {
        'acc' : acc,
        'user': user
    }
    return render(request,'community/myprofile.html',context)


@login_required(login_url='/community/login/')
def deletequote(request,id):
    quote = Quote.objects.get(id=id)
    if quote.quoter != request.user:
        return home(request)
    quote.delete()
    return account(request)


@login_required(login_url='/community/login/')
def deleteser(request,id):
    ser = Service.objects.get(id=id)
    if ser.provider.user != request.user:
        return home(request)
    ser.delete()
    return account(request)


@login_required(login_url='/community/login/')
def deletegood(request,id):
    good = Good.objects.get(id=id)
    if good.provider.user != request.user:
        return home(request)
    good.delete()
    return account(request)


@login_required(login_url='/community/login/')
def add(request):
    acc = Account.objects.get(user=request.user)
    if acc.editor == False:
        return home(request)
    return render(request,'community/addarticle.html')


@login_required(login_url='/community/login/')
def addpost(request):
    acc = Account.objects.get(user=request.user)
    if acc.editor == False:
        return home(request)
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        title = form.cleaned_data['title']
        body = form.cleaned_data['body']
        if form.cleaned_data['feature_pic']:
            feature_pic = request.FILES['feature_pic']
        new_article, created = Post.objects.get_or_create(author=request.user,title=title,body=body,feature_pic=feature_pic)
        return details(request,new_article.id)
    context = {
        'form' : form
    }
    return render(request,'community/addpost.html',context)



@login_required(login_url='/community/login/')
def addpics(request):
    acc = Account.objects.get(user=request.user)
    if acc.editor == False:
        return home(request)
    posts = Post.objects.filter(author=request.user)
    context = {
        'posts' : posts
    }
    return render(request,'community/addpics.html',context)

    
@login_required(login_url='/community/login/')
def addpicsfile(request,id):
    post = Post.objects.get(id=id)
    if post.author != request.user:
        return home(request)
    form = AddPicsForms(request.POST or None,request.FILES or None)
    if form.is_valid():
        for img in request.FILES.getlist('images'):
            PostImage.objects.create(post=post,image=img)
        return myprofile(request)
    context = {
        'form' : form
    }
    return render(request,'community/addpicsfile.html',context)


@login_required(login_url='/community/login/')
def editser(request,id):
    ser = Service.objects.get(id=id)
    if ser.provider.user != request.user:
        return home(request)
    form = ServiceForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        if form.cleaned_data['service']:
            ser.service = form.cleaned_data['service']
        if form.cleaned_data['estimate_prize']:
            ser.estimate_prize = form.cleaned_data['estimate_prize']
        if form.cleaned_data['phone_or_whatsapp_number']:
            ser.phone_or_whatsapp_number = form.cleaned_data['phone_or_whatsapp_number']
        if form.cleaned_data['description']:
            ser.description = form.cleaned_data['description']
        if form.cleaned_data['feature_pic']:
            ser.feature_pic = request.FILES['feature_pic']
        ser.save()
        form = ServiceForm()
        context = {
            'ser' : ser,
            'form' : form,
            'text' : "Changes successfully made."
        }
        return render(request,'community/editser.html',context)
    context = {
        'ser' : ser,
        'form' : form
    }
    return render(request,'community/editser.html',context)


@login_required(login_url='/community/login/')
def editgood(request,id):
    good = Good.objects.get(id=id)
    if good.provider.user != request.user:
        return home(request)
    form = GoodForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        if form.cleaned_data['good']:
            good.good = form.cleaned_data['good']
        if form.cleaned_data['estimate_prize']:
            good.estimate_prize = form.cleaned_data['estimate_prize']
        if form.cleaned_data['phone_or_whatsapp_number']:
            good.phone_or_whatsapp_number = form.cleaned_data['phone_or_whatsapp_number']
        if form.cleaned_data['description']:
            good.description = form.cleaned_data['description']
        if form.cleaned_data['feature_pic']:
            good.feature_pic = request.FILES['feature_pic']
        good.save()
        form = GoodForm()
        context = {
            'good' : good,
            'form' : form,
            'text' : "Changes successfully made."
        }
        return render(request,'community/editgood.html',context)
    context = {
        'good' : good,
        'form' : form
    }
    return render(request,'community/editgood.html',context)


def confirm(request):
    form = ConfirmEmail(request.POST or None)
    data = request.session['data']
    if form.is_valid():
        #userlist = [integer,username,password,first_name,last_name,email,program,dp]
        if int(form.cleaned_data['integer']) == data[0]:
            acc = Account.objects.get(id=data[1])
            acc.activated = True
            return redirect('/community/login/')
    context = {
        'form' : form
    }
    return render(request,'community/confirm.html',context)


@login_required(login_url='/community/login/')
def follow(request,id):
    user = User.objects.get(id=id)
    acc = Account.objects.get(user=user)
    my_acc = Account.objects.get(user=request.user)
    my_acc.following.add(acc.user)
    acc.followers.add(request.user)
    acc.save()
    user.save()
    return studentsearch(request)


@login_required(login_url='/community/login/')
def unfollow(request,id):
    user = User.objects.get(id=id)
    acc = Account.objects.get(user=user)
    my_acc = Account.objects.get(user=request.user)
    my_acc.following.remove(acc.user)
    acc.followers.remove(request.user)
    acc.save()
    user.save()
    return studentsearch(request)


@login_required(login_url='/community/login/')
def userprofile(request,id):
    my_acc = Account.objects.get(user=request.user)
    user = User.objects.get(id=id)
    quotes = Quote.objects.filter(quoter=user)
    sers = Service.objects.filter(provider=user.account)
    goods = Good.objects.filter(provider=user.account)
    posts = Post.objects.filter(author=user)
    context = {
        'my_acc' : my_acc,
        'user' : user,
        'quotes' : quotes,
        'sers' : sers,
        'goods' : goods,
        'posts' : posts,
    }
    return render(request,'community/userprofile.html',context)


@login_required(login_url='/community/login/')
def details(request,id):
    form = CommentForm(request.POST or None)
    post = Quote.objects.get(id=id)
    comments = Comment.objects.filter(quote=post)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        new_comment, created = Comment.objects.get_or_create(quote=post,commenter=request.user,comment=comment)
        form = CommentForm()
        context = {
            'post' : post,
            'comments' : comments,
            'form' : form,
        }
        return render(request,'community/quotedetails.html',context)
    context = {
        'post' : post,
        'comments' : comments,
        'form' : form,
    }
    return render(request,'community/quotedetails.html',context)


@login_required(login_url='/accounts/login/')
def like(request,id):
    post = Quote.objects.get(id=id)
    def like_post(request):
        l , liked = QuoteLike.objects.get_or_create(quote=post,liker=request.user)
        l.save()
    post = Quote.objects.get(id=id)
    like_post(request)
    post.save()
    return redirect('/community/')