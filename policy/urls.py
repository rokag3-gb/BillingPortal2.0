from django.contrib.auth.decorators import login_required
from django.urls import path

from policy import views

urlpatterns = [
    path('confirm/', login_required(views.confirm), name='confirm'),

    path('info/<int:info_number>', login_required(views.info), name='info'),
    path('info/', views.info, name='info-latest'),

    path('info-protection/<int:info_protection_number>', login_required(views.info_protection), name='info-protection'),
    path('info-protection/', views.info_protection, name='info-protection-latest'),
]
