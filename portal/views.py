from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt  
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.sites.shortcuts import get_current_site


sidebar_items = [
    {'name':'대시보드','path':"dashboard"},
    {'name':'지불관리','path':"payment"},
    # {'name':'메시지','path':"messages"}
]

# Create your views here.
@login_required
def index(request: HttpRequest) -> HttpResponse:
    # return render(request, 'portal/index.html')
    return redirect('/dashboard')

@login_required
def preference(request: HttpRequest) -> HttpResponse:
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

@login_required
def payment(request: HttpRequest) -> HttpResponse:
    print(request.META["HTTP_HOST"])
    context = {
        'sidebar': 'payment', 
        'sidebar_items': sidebar_items,
        'payment': getattr(conf, "KICC_EASYPAY", {}),
        'payment_js': getattr(conf, "KICC_EASYPAY_JS_URL", ""),
        'baseurl': getattr(conf, "BASE_URL", "")
     }
    return render(request, 'portal/payment.html', context)

# TODO: iframe 이슈로 임시 예외 처리
# @csrf_exempt 
@login_required
@xframe_options_sameorigin
def payrequest(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/pay/request.html')

# TODO: iframe 이슈로 임시 예외 처리
# @login_required
@csrf_exempt 
@xframe_options_sameorigin
def payresult(request: HttpRequest) -> HttpResponse:
    print(request.method)
    return render(request, 'portal/pay/result.html')