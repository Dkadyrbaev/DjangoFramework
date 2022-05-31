from django.shortcuts import render
from mainapp.models import Product
from django.views.generic import ListView
from django.views.generic.base import TemplateView


class IndexListView(ListView):
    model = Product
    template_name = 'geekshop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexListView, self).get_context_data()
        title = 'Магазин'
        context['title'] = title
        context['products'] = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]

        return context


# def index(request):
#     title = 'магазин'
#     products = Product.objects.all()[:4]
#     context = {
#         'title': title,
#         'products': products,
#         'slogan': 'Супер предложения',
#     }
#     return render(request, 'geekshop/index.html', context)


class ContactsView(TemplateView):
    template_name = 'geekshop/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data()
        context['title'] = 'Контакты'

        return context


# def contacts(request):
#     title = 'контакты'
#     context = {
#         'title': title,
#     }
#     return render(request, 'geekshop/contact.html', context)
