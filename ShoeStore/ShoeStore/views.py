from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Tag, Contact_us
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout



def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product = Product.objects.filter(status='Publish')

    context = {
        'product': product
    }

    return render(request, 'Main/Index.html', context)

def PRODUCT(request):
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_ID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')

    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH') 
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')

    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')

    if CATID:
        product = Product.objects.filter(categories = CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID, status='Publish')
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID, status='Publish')
    elif BRANDID:
        product = Product.objects.filter(brand = BRANDID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='Old').order_by('-id')
    else:
        product = Product.objects.filter(status='Publish')

    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand,
    }

    return render(request, 'Main/product.html', context)

def SEARCH(request):
    query = request.GET.get('query')
    # print(query)
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product': product
    }

    return render(request, 'Main/search.html', context)

def PRODUCT_DETAIL_PAGE(request, id):
    prod = Product.objects.filter(id = id).first()
    context = {
        'prod': prod,
    }
    return render(request, 'Main/product_single.html', context)

def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # print(name, email, subject, message)
        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
        return redirect('home')
    
        '''
            chưa bật được chế độ hỗ trợ truy cập kém an toàn bên thứ 3
        '''

        # subject = subject
        # message = message
        # email_from = settings.EMAIL_HOST_USER
        # try:
        #     send_mail(subject, message, email_from, ['donguyenanh12345@gmail.com'])
        #     contact.save()
        #     return redirect('home')
        # except:
        #     return redirect('contact')

    return render(request, 'Main/contact.html')

# def AUTH(request):
#     return render(request, 'Registration/auth.html')

def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')

    return render(request, 'Registration/auth.html')

def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # 12345 12345
        else:
            return redirect('login')

    return render(request, 'Registration/auth.html')