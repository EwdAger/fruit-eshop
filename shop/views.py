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

    paginator = Paginator(all_products, 4)
    p = request.GET.get('p')
    try:
        products = paginator.page(p)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {"products": products})

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
        user = authenticate(username=username, password=password)
        auth.login(request, user)
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

def add_cart(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, "请登录")
            return redirect('/')
        else:
            username = request.user.username
            item = request.POST.get('item')
            price = request.POST.get('price')

            user_cart = models.Cart.objects.filter(username=username, item=item)
            if user_cart:
                user_cart[0].num += 1
                user_cart[0].save()
                messages.add_message(request, messages.INFO, "商品: " + item + " 添加成功, 数量: " + str(user_cart[0].num))
            else:
                models.Cart.objects.create(username=username, item=item, num=1, price=price)
                messages.add_message(request, messages.INFO, "商品:"+item+"添加成功, 数量: 1")
            return redirect('/')
    else:
        messages.add_message(request, messages.WARNING, "当前页面不存在")
        return render(request, "404.html")

def cart(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, "请登录")
        return redirect('/')
    else:
        username = request.user.username

        items = models.Cart.objects.filter(username=username)

        return render(request, "cart.html", {"username": username, "items": items})

def cart_option(request):
    if request.method == 'POST':
        option = request.POST.get('option')
        username = request.POST.get('username')
        item_name = request.POST.get('item')

        if option == '1':
            item = models.Cart.objects.get(username=username, item=item_name)
            item.num += 1
            item.save()
        elif option == '-1':
            item = models.Cart.objects.get(username=username, item=item_name)
            if item.num == 1:
                item.delete()
            else:
                item.num -= 1
                item.save()
        elif option == '0':
            models.Cart.objects.get(username=username, item=item_name).delete()

        return redirect('/cart')
    else:
        messages.add_message(request, messages.WARNING, "当前页面不存在")
        return render(request, "404.html")

def order(request):
    if request.method == 'POST':
        option = request.POST.get('option')
        username = request.POST.get('username')
        items = models.Cart.objects.filter(username=username)

        if option == 'delete':
            models.Cart.objects.filter(username=username).delete()
            messages.add_message(request, messages.INFO, "购物车已清空")
            return redirect('/')

        elif option == 'submit':
            total = 0
            for item in items:
                total += item.num * item.price
            return render(request, "order.html", {"total": total, "items": items, "username": username})

    else:
        messages.add_message(request, messages.WARNING, "当前页面不存在")
        return render(request, "404.html")
