import json
import os
import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def load_from_json(file_name):
    with open(os.path.join('JSON_PATH', file_name + '.json'), 'r') as infile:
        return json.load(infile)


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'главная'
    products = Product.objects.all()[:3]

    context = {
        'title': title,
        'products': products,
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):
    title = 'Каталог'

    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by(
                'price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True,
                category__is_active=True,
                quantity__gte=1,
            ).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by('price')

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'Детали'

    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': product,
        'same_products': get_same_products(product),
    }
    return render(request, 'mainapp/product.html', context)


def contact(request):
    title = 'о нас'

    locations = load_from_json('contact__locations')

    context = {
        'title': title,
        'locations': locations,
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/contact.html', context)
