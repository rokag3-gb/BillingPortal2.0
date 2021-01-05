from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/login/', auth_views.LoginView.as_view(
        template_name='portal/auth/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/recover/', auth_views.PasswordResetView.as_view(
        template_name='portal/auth/recover.html'), name='password_reset'),
    path('auth/recover/done', auth_views.PasswordResetDoneView.as_view(
        template_name='portal/auth/recover_done.html'), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='portal/auth/reset_confirm.html'), name='password_reset_confirm'),
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='portal/auth/reset_complete.html'), name='password_reset_complete'),
    path('settings/', views.settings, name='settings'),
    path('settings/changepw', auth_views.PasswordChangeView.as_view(
        template_name='portal/settings/changepw.html'), name='password_change'),
    path('settings/changepw/done', auth_views.PasswordChangeDoneView.as_view(
        template_name='portal/settings/pwchanged.html'), name='password_change_done'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),
    path('messages', views.messages, name='messages'),
]
