import datetime
import json

from django.utils import timezone
from django.conf import settings as conf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from zeep import Client, Settings
from django.db.models import Sum

from custom.services import get_organization
from custom.models import Invoice, InvoiceOrder, Payment
from django.db import transaction, IntegrityError
from portal.services import get_sidebar_menu
from django.core.paginator import Paginator

# 결제 화면용 InvoiceOrder, InvoiceOrderDetail 생성 및, 실제 결제화면 보여주는 함수
def payment(request: HttpRequest) -> HttpResponse:
    org = get_organization(request=request)
    if org is None:
        return redirect('/dashboard')
    if request.method == "GET" and (request.GET.get("id") != "" or request.GET.get("id") is not None):
        order_id = request.GET.get("id")
        order_item = InvoiceOrder.objects.get(orderNo=order_id)
        order_details = order_item.getOrderDetails()
        context = {
            'sidebar': 'payment', 
            'sidebar_items': get_sidebar_menu(),
            'invoices': order_details,
            'subtotal': order_item.totalAmount,
            'order_id': order_item.orderNo
        }
        return render(request, 'portal/payment.html', context)
    if request.method == "POST":
        invoice_ids = request.POST.getlist("invoice")
        invoice_details = Invoice.objects.filter(invoiceId__in=invoice_ids, paid=0)
        if len(invoice_details) <= 0:
            return redirect('/invoices?error=alreadypaid')
        else:
            subtotal = invoice_details.aggregate(Sum("rrpAmount"))
            order = InvoiceOrder(
                orderDate = datetime.datetime.now(),
                orderUserId = request.user,
                orgId = org,
                totalAmount = subtotal['rrpAmount__sum'],
                paid = 0,
                isCancel = True,
            )
            order.save()
            order.createDetails(invoice_details)
            return redirect('/payment?id={}'.format(order.orderNo))
    else:
        return redirect('/invoices')

# 입력된 카드정보로 실제 결제를 진행하는 함수
def charge_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # PG 인증서버 통신용 SOAP 클라이언트
        pg_config = getattr(conf, "PG_BACKEND", {})
        settings = Settings(raw_response=False)
        payment_backend = Client(pg_config["SOAP_URL"], settings=settings)
        payment_form = json.loads(request.body.decode("utf-8"))
        try:
            order_item = InvoiceOrder.objects.get(orderNo=payment_form["order_no"], orgId=get_organization(request))
        except InvoiceOrder.DoesNotExist:
            return JsonResponse({'errorMsg':'존재하지 않는 인보이스 주문 항목입니다.'}, status=400)
        valid_until = datetime.datetime.strptime(payment_form['valid_until'], "%Y-%m")
        result = payment_backend.service.KICC_EasyPay_json(
            pg_config["STORE_ID"],
            str(order_item.orderNo),
            "Cloud Service Usage Fee",
            payment_form['card_owner'],
            payment_form['owner_email'],
            payment_form['phone_number'],
            int(order_item.totalAmount),
            # 10,
            payment_form['card_number'],
            valid_until.strftime("%y%m"),
            "0",
            payment_form['card_password'],
            payment_form['owner_proof']
        )
        # print("Statue code: ", result.status_code)
        pgresult = json.loads(result)
        if(pgresult['응답코드']=='0000'):
            try:
                with transaction.atomic():
                    order_item.paid = pgresult['총결제금액']
                    order_item.save()
                    order_details = order_item.getOrderDetails()
                    for detail in order_details:
                        detail.paid = detail.amount
                        detail.save()
                    payment = Payment(
                        paydate = datetime.datetime.strptime(pgresult['승인일시'], "%Y%m%d%H%M%S")
                            .replace(tzinfo=timezone.get_current_timezone()),
                        payamount = int(pgresult['총결제금액']),
                        orderno = order_item, 
                        productname = "Cloud Service Usage Fee",
                        mid = pg_config["STORE_ID"],
                        cardholder = payment_form['card_owner'],
                        auth1 = payment_form['owner_proof'],
                        cardno = pgresult['카드번호'],
                        cardissuer = pgresult['발급사명'],
                        cardacquired = pgresult['매입사명'],
                        auth2 = payment_form['card_password'],
                        expiremmyy = valid_until.strftime("%m%y"),
                        install = pgresult['할부개월'],
                        tid = pgresult['PG거래번호'],
                        apprno = pgresult['승인번호'],
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
                cancel_result = payment_backend.service.KICC_EasyPay_Cancel_json(
                    pg_config["STORE_ID"],
                    "40",
                    pgresult["PG거래번호"],
                    str(order_item.orderNo),
                    pgresult["총결제금액"],
                    request.user.username,
                    "Payment data persist error",
                )
                pg_cancel = json.loads(cancel_result)
                return JsonResponse({"errorMsg":"결제 완료 처리 중 오류가 발생하여, 결제가 취소되었습니다."}, status=500)
        else:
            return JsonResponse({"errorMsg":pgresult['응답메시지']}, status=400)

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
    result = result.order_by("-paydate")
    paginator = Paginator(result, 20) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            'sidebar': 'payment_history', 
            'sidebar_items': get_sidebar_menu(),
            'page_obj': page_obj
        }
    return render(request, 'portal/payment_history.html', context)