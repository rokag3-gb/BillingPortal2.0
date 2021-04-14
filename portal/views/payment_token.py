
import json, datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError

from custom.services import get_organization
import requests
from django.views.decorators.clickjacking import xframe_options_sameorigin
from custom.models import Billkey, InvoiceOrder, Payment

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
    if res.status_code == requests.codes.ok:
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

def charge_token_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # PG 인증서버 통신용 SOAP 클라이언트
        pg_config = getattr(settings, "PG_BACKEND", {})
        payment_form = json.loads(request.body.decode("utf-8"))
        valid_until = datetime.datetime.strptime(payment_form['valid_until'], "%Y-%m")

        try:
            order_item = InvoiceOrder.objects.get(orderNo=payment_form["order_no"], orgId=get_organization(request))
        except InvoiceOrder.DoesNotExist:
            return JsonResponse({'errorMsg':'존재하지 않는 인보이스 주문 항목입니다.'}, status=400)

        payresult = requests.post(pg_config["PG_API_URL"]+"/pay/onetime", json={
            "storeId": pg_config["STORE_ID"],
            "orderNumber": str(order_item.orderNo),
            "productName": "Cloud Service Usage Fee",
            "ownerName": payment_form['card_owner'],
            "ownerEmail": payment_form['owner_email'],
            "ownerPhoneNumber": payment_form['phone_number'],
            "cardNumber": payment_form['card_number'],
            "cardValidThru": valid_until.strftime("%y%m"),
            "isNoInterestPayment": False,
            "cardPassword": payment_form['card_password'],
            "cardOwnerIdentifyCode": payment_form['owner_proof'],
            "paymentAmount": int(order_item.totalAmount)
            })
        
        pgresult = payresult.json()
        if payresult.status_code == requests.codes.ok:
            try:
                with transaction.atomic():
                    order_item.paid = int(pgresult['totalPaymentAmount'])
                    order_item.save()
                    order_details = order_item.getOrderDetails()
                    for detail in order_details:
                        detail.paid = detail.amount
                        detail.save()
                    payment = Payment(
                        paydate = datetime.datetime.strptime(pgresult['approvedAt'], "%Y%m%d%H%M%S")
                            .replace(tzinfo=timezone.get_current_timezone()),
                        payamount = pgresult['totalPaymentAmount'],
                        orderno = order_item, 
                        productname = "Cloud Service Usage Fee",
                        mid = pg_config["STORE_ID"],
                        cardholder = payment_form['card_owner'],
                        auth1 = payment_form['owner_proof'],
                        cardno = pgresult['cardNumber'],
                        cardissuer = pgresult['cardIssuerName'],
                        cardacquired = pgresult['cardAcquirerName'],
                        auth2 = payment_form['card_password'],
                        expiremmyy = valid_until.strftime("%m%y"),
                        install = pgresult['cardInstallPeriod'],
                        tid = pgresult['txNumber'],
                        apprno = pgresult['approvalNumber'],
                        email = payment_form['owner_email'],
                        cellphone = payment_form['phone_number'],
                        iscancel = False
                    )
                    payment.save()
                    return JsonResponse(pgresult)
            except IntegrityError as error:
                print("Transaction error: ")
                print(error)
                # 결제 취소 호출

                cancelresult = requests.put(pg_config["PG_API_URL"]+"/pay/onetime", json={
                   "storeId": pg_config["STORE_ID"],
                    "cancelType": 40,
                    "txNumber": pgresult['txNumber'],
                    "orderNumber": str(order_item.orderNo),
                    "cancelAmount": pgresult['totalPaymentAmount'],
                    "requesterID": request.user.username,
                    "cancelReason": "Payment data persist error",
                })
                return JsonResponse({"errorMsg":"결제 완료 처리 중 오류가 발생하여, 결제가 취소되었습니다."}, status=500)
        else:
            return JsonResponse({"errorMsg":pgresult['resultMessage']}, status=payresult.status_code)