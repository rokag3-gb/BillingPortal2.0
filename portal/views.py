from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required

sidebar_items = [
    {'name':'대시보드','path':"dashboard"},
    # {'name':'프로필','path':"profile"},
    # {'name':'메시지','path':"messages"}
]

# Create your views here.
@login_required
def index(request: HttpRequest) -> HttpResponse:
    # return render(request, 'portal/index.html')
    return redirect('/')

@login_required
def settings(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/settings/index.html')

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/dashboard.html', {'sidebar': 'dashboard', 'sidebar_items': sidebar_items })

@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/profile.html', {'sidebar': 'profile', 'sidebar_items': sidebar_items})

@login_required
def messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/messages.html', {'sidebar': 'messages', 'sidebar_items': sidebar_items})

