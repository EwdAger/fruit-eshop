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
            sku = request.POST.get('sku')

            if int(sku) <= 0:
                messages.add_message(request, messages.WARNING, "商品库存不足 1个，无法加入购物车")
                return redirect('/')
            user_cart = models.Cart.objects.filter(username=username, item=item)
            good = models.Product.objects.get(name=item)
            good.sku -= 1
            good.save()
            if user_cart:
                user_cart[0].num += 1
                user_cart[0].save()
                messages.add_message(request, messages.INFO, "商品: " + item + " 添加成功, 数量: " + str(user_cart[0].num))
            else:
                models.Cart.objects.create(username=username, item=item, num=1, price=price)
                messages.add_message(request, messages.INFO, "商品:"+item+" 添加成功, 数量: 1")
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

        good = models.Product.objects.get(name=item_name)
        if option == '1':
            if good.sku > 0:
                good.sku -= 1
                good.save()
                item = models.Cart.objects.get(username=username, item=item_name)
                item.num += 1
                item.save()
            else:
                messages.add_message(request, messages.WARNING, "商品数量不足 1个")
        elif option == '-1':
            item = models.Cart.objects.get(username=username, item=item_name)
            good.sku += 1
            good.save()
            if item.num == 1:
                item.delete()
            else:
                item.num -= 1
                item.save()
        elif option == '0':
            item = models.Cart.objects.get(username=username, item=item_name)
            good.sku += item.num
            good.save()
            item.delete()

        return redirect('/cart')
    else:
        messages.add_message(request, messages.WARNING, "当前页面不存在")
        return render(request, "404.html")

def order(request):
    if request.method == 'POST':
        option = request.POST.get('option')
        username = request.POST.get('username')
        items = models.Cart.objects.filter(username=username)
        good = models.Product.objects.get(name=items[0].item)

        if option == 'delete':
            good.sku += items[0].num
            good.save()
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

def add_order(request):
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        goods = models.Cart.objects.filter(username=username)
        item = []

        for good in goods:
            temp = str(good.item) + 'x' + str(good.num)
            item.append(temp)
        item = "\n".join(item)
        models.Order.objects.create(username=username, name=name, location=location, phone=phone, item=item)
        goods.delete()
        messages.add_message(request, messages.INFO, "订单已提交")
        return redirect('/')

    else:
        messages.add_message(request, messages.WARNING, "当前页面不存在")
        return render(request, "404.html")