from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from custom.services import get_organization
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
    billkeys = Billkey.objects.filter(orgid=get_organization(request))
    return render(request, 'portal/manage_payments.html',
        {'payments': billkeys,
        'card_error': card_error,
        'card_message': card_message})

@csrf_exempt
@xframe_options_sameorigin
def cert_form(request):  
    pg_config = getattr(settings, "PG_BACKEND", {})
    baseurl = getattr(settings, "BASE_URL", "")
    print(baseurl)
    return render(request, 'portal/billkey/cert.html', {"STORE_ID": pg_config["STORE_ID"], "BASE_URL": baseurl})

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
    if resdata["resultCode"] == "0000":
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
    else:
        return render(request, 'portal/billkey/token_error.html', {"ERROR_CODE": resdata["resultCode"]})