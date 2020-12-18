from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view())
]