"""Mate365BillingPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path, include

from custom.views import CustomLoginView
from portal.views import payment, dashboard, index, preference, profile, messages

urlpatterns = [
    # FIXME: next 파라미터가 동작하지 않음
    path('billingadmin/login/', LoginView.as_view(template_name="registration/login.html", ), name='login'),
    path('billingadmin/', admin.site.urls),

    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/', include('django.contrib.auth.urls')),

    path('organization/', include('custom.urls')),
    path('powerbi/', include('powerbi.urls')),

    path('payment/', login_required(payment), name='payment'),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('settings/', preference, name='settings'),
    path('profile/', profile, name='profile'),
    path('messages/', messages, name='messages'),
    path('', index, name='index'),
]
