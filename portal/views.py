import datetime
import json

from django.conf import settings as conf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from zeep import Client, Settings

# PG 인증서버 통신용 SOAP 클라이언트
from custom.services import get_organization

pg_config = getattr(conf, "PG_BACKEND", {})
settings = Settings(raw_response=False)
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


def dashboard(request: HttpRequest) -> HttpResponse:
    org = get_organization(request=request)

    if org is None:
        return render(request, 'portal/dashboard-none-org.html', {'sidebar': 'dashboard', 'sidebar_items': sidebar_items})

    return render(request, 'portal/dashboard.html', {'sidebar': 'dashboard', 'sidebar_items': sidebar_items })


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/profile.html', {'sidebar': 'profile', 'sidebar_items': sidebar_items})

@login_required
def messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/messages.html', {'sidebar': 'messages', 'sidebar_items': sidebar_items})


def payment(request: HttpRequest) -> HttpResponse:
    org = get_organization(request=request)

    if org is None:
        return redirect('/dashboard')

    if(request.method == "POST"):
        payment_form = json.loads(request.body.decode("utf-8"))
        print(payment_form)
        result = payment_backend.service.KICC_EasyPay_json(
            pg_config["STORE_ID"],
            "123",
            "클라우드사용비용",
            payment_form['card_owner'],
            payment_form['owner_email'],
            payment_form['phone_number'],
            100,
            payment_form['card_number'],
            datetime.datetime.strptime(payment_form['valid_until'], "%Y-%m").strftime("%y%m"),
            "0",
            payment_form['card_password'],
            datetime.date.fromisoformat(payment_form['owner_birthday']).strftime("%y%m%d")
        )
        # print("Statue code: ", result.status_code)
        pgresult = json.loads(result)
        if(pgresult['응답코드']=='0000'):
            return JsonResponse(pgresult)
        else:
            return JsonResponse(pgresult, status=400)
    else:
        context = {
            'sidebar': 'payment', 
            'sidebar_items': sidebar_items,
        }
        return render(request, 'portal/payment.html', context)