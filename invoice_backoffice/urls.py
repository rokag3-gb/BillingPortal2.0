from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('management/', views.index),
  path('report/<str:id>/', views.report)
]