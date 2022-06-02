import json
import os
import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import Product, ProductCategory
from django.views.generic import DetailView, ListView
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category {pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product {pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = 'products_in_category_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category=pk, is_active=True, category__is_active=True).order_by('price')


def load_from_json(file_name):
    with open(os.path.join('JSON_PATH', file_name + '.json'), 'r') as infile:
        return json.load(infile)


# def get_hot_product(pk):
#     start = 0
#     stop = len(Product.objects.filter(category=pk)) - 1
#     hot_product = Product.objects.filter(category=pk)[randint(start, stop)]
#
#     return hot_product
#
#
# def get_same_products(hot_product):
#     same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
#     return same_products

def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).order_by('price')

    return same_products


class ProductsView(ListView):
    model = Product
    paginate_by = 2
    template_name = 'mainapp/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsView, self).get_context_data()
        if 'pk' in kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 0
        title = 'Каталог v2.0'
        context['links_menu'] = ProductCategory.objects.all()

        context['title'] = title

        if pk == 0:
            context['category'] = {'name': 'все'}
            products = get_products_ordered_by_price()
        else:
            context['category'] = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)
        context['hot_product'] = hot_product
        context['same_products'] = same_products

        context['pk'] = pk
        context['products'] = products
        return context



# @cache_page(3600)
# def products(request, pk=None, page=1):
#     title = 'Каталог'
#
#     links_menu = get_links_menu()
#
#     if pk is not None:
#         if pk == 0:
#             category = {'pk': 0, 'name': 'все'}
#             products = get_products_ordered_by_price()
#         else:
#             category = get_category(pk)
#             products = get_products_in_category_ordered_by_price(pk)
#
#         paginator = Paginator(products, 2)
#         try:
#             products_paginator = paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator = paginator.page(1)
#         except EmptyPage:
#             products_paginator = paginator.page(paginator.num_pages)
#
#         context = {
#             'title': title,
#             'links_menu': links_menu,
#             'category': category,
#             'products': products_paginator,
#         }
#         return render(request, 'mainapp/products.html', context)
#
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)[:3]
#     products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by('price')[:3]
#
#     context = {
#         'title': title,
#         'links_menu': links_menu,
#         'hot_product': hot_product,
#         'same_products': same_products,
#         'products': products,
#     }
#
#     return render(request, 'mainapp/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    title = 'Страница продукта'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        links_menu = get_links_menu()
        same_products = Product.objects.filter(category=self.object.category)
        context['links_menu'] = links_menu
        context['same_products'] = same_products
        return context


