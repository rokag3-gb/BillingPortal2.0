
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
from custom.models import Billkey, InvoiceOrder, Payment, UserProfile

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
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.phone.strip() and user_profile.location.strip():
        return render(request, 'portal/billkey/cert.html', {"STORE_ID": pg_config["STORE_ID"], "BASE_URL": baseurl})
    return render(request, 'portal/billkey/token_error.html')
    

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
                reguserid=request.user,
                issuercode=resdata["cardIssuerCode"],
                issuername=resdata["cardIssuerName"],
                acquirercode=resdata["cardAcquirerCode"],
                acquirername=resdata["cardAcquirerName"]
            ).save()
        
        print(res.json())
        return redirect("manage_payments")
    else:
        return render(request, 'portal/billkey/token_error.html', {
                "ERROR_CODE": resdata["resultCode"],
                "ERROR_MSG": resdata["resultMessage"]})

def charge_token_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # PG 인증서버 통신용 SOAP 클라이언트
        pg_config = getattr(settings, "PG_BACKEND", {})
        payment_form = json.loads(request.body.decode("utf-8"))

        if not request.user.check_password(payment_form["user_password"]):
            return JsonResponse({'errorMsg':' 틀린 사용자 로그인 암호 입니다.'}, status=400)

        try:
            order_item = InvoiceOrder.objects.get(orderNo=payment_form["order_no"], orgId=get_organization(request))
        except InvoiceOrder.DoesNotExist:
            return JsonResponse({'errorMsg':'존재하지 않는 인보이스 주문 항목입니다.'}, status=400)

        try:
            billkey = Billkey.objects.get(seq=payment_form["payment_method_id"], orgid=get_organization(request), isactive=True)
        except Billkey.DoesNotExist:
            return JsonResponse({'errorMsg':'존재하지 않거나 비활성화된 결제수단 입니다.'}, status=400)
        
        try:
            user_profile = UserProfile.objects.get(user=billkey.reguserid)
            if not user_profile.phone.strip() or not user_profile.location.strip():
                return JsonResponse({'errorMsg':'해당 결제수단을 등록한 사용자 계정에 청구지 주소와 연락처 정보가 없습니다. 주소 및 연락저 정보가 있어야 결제할 수 있습니다.'}, status=400)
        except Billkey.DoesNotExist:
            return JsonResponse({'errorMsg':'해당 결제수단을 등록한 사용자가 존재하지 않습니다. 결제수단을 삭제 후 다시 등록하세요.'}, status=400)
        

        payresult = requests.post(pg_config["PG_API_URL"]+"/pay/withtoken", json={
            "storeId": pg_config["STORE_ID"],
            "orderNumber": str(order_item.orderNo),
            "productName": "Cloud Service Usage Fee",
            "ownerID": billkey.reguserid.get_username(),
            "ownerName": billkey.reguserid.get_full_name(),
            "ownerEmail": billkey.reguserid.email,
            "ownerPhoneNumber": user_profile.phone,
            "isNoInterestPayment": False,
            "paymentToken": billkey.billkey,
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
                        detail.isCancel = False
                        detail.save()
                    payment = Payment(
                        paydate = datetime.datetime.strptime(pgresult['approvedAt'], "%Y%m%d%H%M%S")
                            .replace(tzinfo=timezone.get_current_timezone()),
                        payamount = pgresult['totalPaymentAmount'],
                        orderno = order_item, 
                        productname = "Cloud Service Usage Fee",
                        mid = pg_config["STORE_ID"],
                        cardholder = billkey.reguserid.get_full_name(),
                        billkey = billkey.billkey,
                        cardissuer = pgresult['cardIssuerName'],
                        cardacquired = pgresult['cardAcquirerName'],
                        install = pgresult['cardInstallPeriod'],
                        tid = pgresult['txNumber'],
                        apprno = pgresult['approvalNumber'],
                        email = billkey.reguserid.email,
                        cellphone = user_profile.phone,
                        iscancel = False
                    )
                    payment.save()
                    return JsonResponse(pgresult)
            except IntegrityError as error:
                print("Transaction error: ")
                print(error)
                # 결제 취소 호출

                cancelresult = requests.put(pg_config["PG_API_URL"]+"/pay/withtoken", json={
                    "storeId": pg_config["STORE_ID"],
                    "cancelType": 40,
                    "txNumber": pgresult['txNumber'],
                    "orderNumber": str(order_item.orderNo),
                    "requesterID": request.user.username,
                    "cancelReason": "Payment data persist error",
                    })
                return JsonResponse({"errorMsg":"결제 완료 처리 중 오류가 발생하여, 결제가 취소되었습니다."}, status=500)
        else:
            return JsonResponse({"errorMsg":"{}({})".format(pgresult['resultMessage'], pgresult['resultCode'])}, status=payresult.status_code)