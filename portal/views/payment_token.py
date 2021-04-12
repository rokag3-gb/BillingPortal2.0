import datetime
import json

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db.models import Sum

from custom.services import get_organization
from custom.models import Invoice, InvoiceOrder, Payment
from django.db import transaction, IntegrityError
import requests
from django.views.decorators.clickjacking import xframe_options_sameorigin
from custom.models import Billkey

def manage_payments(request: HttpRequest) -> HttpResponse:
    card_error = None
    card_message = None
    if request.method == "POST":
        if request.POST.get("action", "") == "delete":
            try:
                payment = Billkey.objects.get(seq=int(request.POST.get("id")))
                if payment.orgid == request.user.org_last_selected:
                    payment.delete()
                    card_message = "카드 삭제가 완료되었습니다."
                else:
                    card_error = "해당 카드가 존재하지 않습니다."
            except:
                card_error = "해당 카드가 존재하지 않습니다."
        # else:
            # print(request.POST.get('valid_until'))
            # valid_until = datetime.datetime.strptime(request.POST.get('valid_until'), "%Y-%m")
            # Billkey(
            #     orgid=get_organization(request),
            #     isactive=True,
            #     billkey="123123",
            #     alias=request.POST.get("card_alias"),
            #     auth1=datetime.date.fromisoformat(request.POST.get('owner_birthday')).strftime("%y%m%d"),
            #     cardno=request.POST.get("card_number"),
            #     auth2=request.POST.get("card_password"),
            #     expiremm=valid_until.strftime("%m"),
            #     expireyy=valid_until.strftime("%y"),
            #     reguserid=request.user
            # ).save()
            # card_message = "카드가 등록되었습니다."
    billkeys = Billkey.objects.filter(orgid=get_organization(request))
    return render(request, 'portal/manage_payments.html',
        {'payments': billkeys,
        'card_error': card_error,
        'card_message': card_message})

@csrf_exempt
@xframe_options_sameorigin
def cert_form(request):  
    pg_config = getattr(settings, "PG_BACKEND", {})
    return render(request, 'portal/billkey/cert.html', {"STORE_ID": pg_config["STORE_ID"]})

@csrf_exempt
@xframe_options_sameorigin
def issue_param(request):  # 인증 요청 iframe/submit 페이지 호출
    return render(request, 'portal/billkey/issue_param.html')

@csrf_exempt
@xframe_options_sameorigin
def issue_param_callback(request):
    return render(request, 'portal/billkey/issue_param_callback.html')

@xframe_options_sameorigin
def issue_token(request):
    pg_config = getattr(settings, "PG_BACKEND", {})
    res = requests.post(pg_config["PG_API_URL"]+"/token", json={
            "storeId": request.POST.get('EP_mall_id'),
            "orderNumber": request.POST.get('EP_order_no'),
            "traceNumber": request.POST.get("EP_trace_no"),
            "sessionKey":request.POST.get("EP_sessionkey"),
            "encryptedRegistrationParams": request.POST.get("EP_encrypt_data")
           })
    resdata = res.json()
    print(issue_token)
    Billkey(
            orgid=get_organization(request),
            isactive=True,
            billkey=resdata["paymentToken"],
            alias=request.POST.get("EP_card_nick"),
            auth1="",
            cardno="",
            auth2="",
            expiremm="",
            expireyy="",
            reguserid=request.user
        ).save()
    
    print(res.json())
    return redirect("manage_payments")