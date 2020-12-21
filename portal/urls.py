from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='portal/auth/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view()),
    path('auth/recover/', auth_views.PasswordResetView.as_view(template_name='portal/auth/recover.html'), name='recover'),
    path('auth/recover/done', auth_views.PasswordResetDoneView.as_view(template_name='portal/auth/recover_done.html'))
]