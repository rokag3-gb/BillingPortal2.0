from django.contrib.auth.decorators import login_required
from django.urls import path

from custom import views

urlpatterns = [
    path('', login_required(views.list_org), name='list-org'),
    path('switch_to/<slug:organization_slug>', login_required(views.switch_to_org), name='switch-to-org'),
]
