from venv import create
from django.shortcuts import render
from .models import Service, Good, Picture, GoodPicture
from .forms import PostBizForm, PostProductForm, SearchForm
from community.models import Account
from django.contrib.auth.decorators import login_required


@login_required(login_url='/community/login/')
def home(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        search = form.cleaned_data['search']
        sers = Service.objects.filter(service__icontains=search).order_by("-date_added")
        form = SearchForm()
        context = {
            'form' : form,
            'sers' : sers
        }
        return render(request,'biz/home.html',context)
    sers = Service.objects.all().order_by("-date_added")
    context = {
        'sers' : sers,
        'form' : form
    }
    return render(request,'biz/home.html',context)

@login_required(login_url='/community/login/')
def goods(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        search = form.cleaned_data['search']
        goods = Good.objects.filter(good__icontains=search).order_by("-date_added")
        form = SearchForm()
        context = {
            'form' : form,
            'sers' : goods
        }
        return render(request,'biz/goods.html',context)
    goods = Good.objects.all().order_by("-date_added")
    context = {
        'sers' : goods,
        'form' : form
    }
    return render(request,'biz/goods.html',context)


@login_required(login_url='/community/login/')
def details(request,id):
    service = Service.objects.get(id=id)
    pics = Picture.objects.filter(service=service)
    context = {
        'service' : service,
        'pics' : pics
    }
    return render(request,'biz/details.html',context)


@login_required(login_url='/community/login/')
def good(request,id):
    service = Good.objects.get(id=id)
    pics = GoodPicture.objects.filter(good=service)
    context = {
        'service' : service,
        'pics' : pics
    }
    return render(request,'biz/details.html',context)

@login_required(login_url='/community/login/')
def post(request):
    return render(request,'biz/post.html')

@login_required(login_url='/community/login/')
def postservice(request):
    form = PostBizForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        acc = Account.objects.get(user=request.user)
        service = form.cleaned_data['service']
        prize = form.cleaned_data['estimate_prize']
        phone = form.cleaned_data['phone_or_whatsapp_number']
        des = form.cleaned_data['description']
        if form.cleaned_data['feature_pic'] != None:
            pic = request.FILES['feature_pic']
        new_service, created = Service.objects.get_or_create(provider=acc,service=service,estimate_prize=prize,phone_or_whatsapp_number=phone,description=des,feature_pic=pic)
        return details(request,new_service.id)
    context = {
        'form' : form
    }
    return render(request,'biz/postservice.html',context)

@login_required(login_url='/community/login/')
def postproduct(request):
    form = PostProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        acc = Account.objects.get(user=request.user)
        service = form.cleaned_data['good']
        prize = form.cleaned_data['estimate_prize']
        phone = form.cleaned_data['phone_or_whatsapp_number']
        des = form.cleaned_data['description']
        if form.cleaned_data['feature_pic'] != None:
            pic = request.FILES['feature_pic']
        new_service, created = Good.objects.get_or_create(provider=acc,good=service,estimate_prize=prize,phone_or_whatsapp_number=phone,description=des,feature_pic=pic)
        return good(request,new_service.id)
    context = {
        'form' : form
    }
    return render(request,'biz/postproduct.html',context)