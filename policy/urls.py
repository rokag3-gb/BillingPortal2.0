from django.contrib.auth.decorators import login_required
from django.urls import path

from policy import views

urlpatterns = [
    path('confirm/', login_required(views.confirm), name='confirm'),

    path('terms_of_use/<int:number>', login_required(views.terms_of_use), name='terms-of-use'),
    path('terms_of_use/', views.terms_of_use, name='terms-of-use-latest'),

    path('info_gathering/<int:number>', login_required(views.info_gathering), name='info-gathering'),
    path('info_gathering/', views.info_gathering, name='info-gathering-latest'),

    path('using_credit_card/<int:number>', login_required(views.using_credit_card), name='using-credit-card'),
    path('using_credit_card/', views.using_credit_card, name='using-credit-card-latest'),
]
