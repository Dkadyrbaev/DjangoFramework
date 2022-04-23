from django.urls import path

from ordersapp.views import (
    OrderListView,
    OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderUpdateView,
    order_forming_complete,
)

app_name = "ordersapp"

urlpatterns = [
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('', OrderListView.as_view(), name='main'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_read'),
]