from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand


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

    if CATID:
        product = Product.objects.filter(categories = CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID, status='Publish')
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID, status='Publish')
    elif BRANDID:
        product = Product.objects.filter(brand = BRANDID, status='Publish')
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