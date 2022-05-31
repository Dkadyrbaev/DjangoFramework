from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from mainapp.views import ProductDetailView, ProductsView

app_name = 'mainapp'
urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    # path('', cache_page(3600)(ProductsView.as_view()), name='index'),
    # path('', products, name='index'),
    # re_path(r'^$', products, name='index'),
    path('category/<int:pk>/', ProductsView.as_view(), name='category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('category/<int:pk>/page/<int:page>/', ProductsView.as_view(), name='page'),
]
