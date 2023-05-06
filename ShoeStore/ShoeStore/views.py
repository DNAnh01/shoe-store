from django.shortcuts import render, redirect
from store_app.models import Product


def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product = Product.objects.all()

    context = {
        'product': product
    }

    return render(request, 'Main/Index.html', context)