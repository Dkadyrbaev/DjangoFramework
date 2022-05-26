import json
import os
from random import randint

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView


def load_from_json(file_name):
    with open(os.path.join('JSON_PATH', file_name + '.json'), 'r') as infile:
        return json.load(infile)


def get_hot_product():
    start = 0
    stop = len(Product.objects.all()) - 1
    hot_product = Product.objects.all()[randint(start, stop)]

    return hot_product


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products


class ProductsView(ListView):
    model = Product
    title = 'Каталог v2.0'
    paginate_by = 2  # как заставить его работать на same_products?
    template_name = 'mainapp/products.html'

    def get_context_data(self, *, pk=None, page=1, object_list=None, **kwargs):
        context = super(ProductsView, self).get_context_data()
        context['links_menu'] = ProductCategory.objects.all()
        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)
        context['hot_product'] = hot_product
        context['same_products'] = same_products

        return context


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
    same_products = get_same_products(hot_product)[:3]
    products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by('price')[:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
    }

    return render(request, 'mainapp/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    title = 'Страница продукта'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        links_menu = ProductCategory.objects.all()
        same_products = Product.objects.filter(category=self.object.category)[:2]
        context['links_menu'] = links_menu
        context['same_products'] = same_products
        return context


