from django.urls import path, re_path
from mainapp.views import products, ProductDetailView, ProductsView

app_name = 'mainapp'
urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    # re_path(r'^$', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('category/<int:pk>/page/<int:page>/', products, name='page'),
]
