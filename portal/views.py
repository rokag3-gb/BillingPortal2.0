from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt  
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf
import json
import xml.etree.ElementTree as ET
from zeep import Client, Settings

pg_config = getattr(conf, "PG_BACKEND", {})
settings = Settings(raw_response=True)
payment_backend = Client(pg_config["SOAP_URL"], settings=settings)

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
    if(request.method == "POST"):
        payment_form = json.loads(request.body.decode("utf-8"))
        result = payment_backend.service.KICC_EasyPay_json(
            pg_config["STORE_ID"],
            "123",
            "클라우드사용비용",
            payment_form['card_owner'],
            payment_form['owner_email'],
            payment_form['card_number'],
            3000,
            payment_form['phone_number'],
            "22" + "10",
            "0",
            payment_form['card_password'],
            "961008" 
        )
        return JsonResponse({"result":"ok"})
    else:
        context = {
            'sidebar': 'payment', 
            'sidebar_items': sidebar_items,
        }
        return render(request, 'portal/payment.html', context)