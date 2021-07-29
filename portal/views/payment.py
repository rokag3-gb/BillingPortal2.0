import datetime
import json

from django.utils import timezone
from django.conf import settings as conf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.forms.models import model_to_dict


from custom.services import get_organization
from custom.models import Invoice, InvoiceOrder, Payment, Billkey
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator
from django.views.decorators.clickjacking import xframe_options_sameorigin
import requests


# 결제 화면용 InvoiceOrder, InvoiceOrderDetail 생성 및, 실제 결제화면 보여주는 함수
def payment(request: HttpRequest) -> HttpResponse:
    org = get_organization(request=request)
    if org is None:
        return redirect('/dashboard')
    if request.method == "GET" and (request.GET.get("id") != "" or request.GET.get("id") is not None):
        order_id = request.GET.get("id")
        order_item = InvoiceOrder.objects.get(orderNo=order_id)
        order_details = order_item.getOrderDetails()
        billkeys = Billkey.objects.filter(orgid=get_organization(request))
        context = {
            'invoices': order_details,
            'subtotal': order_item.totalAmount,
            'order_id': order_item.orderNo,
            'token_payments': billkeys,
        }
        return render(request, 'portal/payment.html', context)
    if request.method == "POST":
        invoice_ids = request.POST.getlist("invoice")
        invoice_details = Invoice.objects.filter(invoiceId__in=invoice_ids, paid=0)
        if len(invoice_details) <= 0:
            return redirect('/invoice_list?error=alreadypaid')
        else:
            subtotal = invoice_details.aggregate(Sum("rrp_amount_pretax"))
            order = InvoiceOrder(
                orderDate = datetime.datetime.now(),
                orderUserId = request.user,
                orgId = org,
                totalAmount = subtotal['rrp_amount_pretax__sum'],
                paid = 0,
                isCancel = True,
            )
            order.save()
            order.createDetails(invoice_details)
            return redirect('/payment?id={}'.format(order.orderNo))
    else:
        return redirect('/invoices')

# 입력된 카드정보로 실제 결제를 진행하는 함수
def charge_oneimte_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # PG 인증서버 통신용 SOAP 클라이언트
        pg_config = getattr(conf, "PG_BACKEND", {})
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

def payment_history(request: HttpRequest) -> HttpResponse:
    date_start = request.GET.get('date_start', default=None)
    date_end = request.GET.get('date_end', default=None)
    result = Payment.objects.filter(orderno__orgId=get_organization(request))
    if date_start:
        date_start = datetime.datetime.strptime(date_start, "%Y-%m")
        result = result.filter(paydate__gte=date_start)
    if date_end:
        date_end = datetime.datetime.strptime(date_end, "%Y-%m")
        date_end = date_end.replace(month=date_end.month+1) - datetime.timedelta(days=1)
        result = result.filter(paydate__lte=date_end)
    if date_start == None and date_end == None:
        date_end = datetime.datetime.now()
        date_start = date_end - datetime.timedelta(days=32)
        date_start = date_start.replace(day=1)
        result = result.filter(paydate__gte=date_start)
        result = result.filter(paydate__lte=date_end)
    result = result.order_by("-paydate")
    paginator = Paginator(result, 20) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'current_filter': {
            'date_start': date_start.strftime("%Y-%m"),
            'date_end': date_end.strftime("%Y-%m")
        }
    }
    return render(request, 'portal/payment_history.html', context)

@xframe_options_sameorigin
def payment_details(request: HttpRequest) -> HttpResponse:
    orderNo = request.GET.get("id", default=None)
    if orderNo:
        try:
            orderItem = InvoiceOrder.objects.get(orderNo=orderNo, orgId=get_organization(request))
            details = orderItem.getOrderDetails().values()

            model_to_dict(orderItem, fields=["orderNo"])
            return JsonResponse({
                'order_summary': model_to_dict(orderItem, 
                    fields=["orderNo", "orderDate", "totalAmount", "paid"]),
                'order_details': list(details),
            })
        except InvoiceOrder.DoesNotExist:
            pass
    return JsonResponse({'order_summary':[], 'order_details':[]})