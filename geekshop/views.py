from django.shortcuts import render
from mainapp.models import Product


def index(request):
    title = 'магазин'
    products = Product.objects.all()[:4]
    context = {
        'title': title,
        'products': products,
        'slogan': 'Супер предложения',
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
    }
    return render(request, 'geekshop/contact.html', context)
