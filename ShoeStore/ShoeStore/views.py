from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Tag, Contact_us


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
    return render(request, 'Main/contact.html')