from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import redirect

from shop import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def index(request):
    all_products = models.Product.objects.all()

    paginator = Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator.page(p)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'index.html', locals())

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign_up.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            messages.add_message(request, messages.WARNING, '已存在该用户')
            return render(request, 'sign_up.html')
        user = User.objects.create_user(username,username,password)
        user.save()
        messages.add_message(request, messages.SUCCESS, '注册成功')
        return redirect('/')

def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, '登陆成功')
            return redirect('/')
        else:
            messages.add_message(request, messages.WARNING, '用户不存在或者账号密码错误')
            return render(request, 'login.html')

def log_out(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功注销")
    return redirect('/')