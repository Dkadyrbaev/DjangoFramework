from django.urls import path
from .views import edit, UserRegisterView, UserLoginView, UserLogoutView, UserUpdateView
from authapp.views import verify

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit/', edit, name='edit'),

    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
