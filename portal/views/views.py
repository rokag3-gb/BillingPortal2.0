import datetime

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from custom.services import get_organization
from custom.models import Invoice, Billkey, Organization

def index(request: HttpRequest) -> HttpResponse:
    # return render(request, 'portal/index.html')
    return redirect('/dashboard')


@login_required
def preference(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/settings/index.html')


def dashboard(request: HttpRequest) -> HttpResponse:
    org = get_organization(request=request)
    if org is None:
        return render(request, 'portal/dashboard-none-org.html')
    return render(request, 'portal/dashboard.html')

def invoices(request: HttpRequest) -> HttpResponse:
    date_start = request.GET.get('date_start', default=None)
    date_end = request.GET.get('date_end', default=None)
    result = Invoice.objects.filter(orgId=get_organization(request))
    if date_start:
        date_start = datetime.datetime.strptime(date_start, "%Y-%m")
        result = result.filter(invoiceDate__gte=date_start)
    if date_end:
        date_end = datetime.datetime.strptime(date_end, "%Y-%m")
        date_end = date_end.replace(month=date_end.month + 1) - datetime.timedelta(days=1)
        result = result.filter(invoiceDate__lte=date_end)
    if date_start == None and date_end == None:
        date_end = datetime.datetime.now()
        date_start = date_end.replace(month=date_end.month-1) - datetime.timedelta(days=1)
        result = result.filter(invoiceDate__gte=date_start)
        result = result.filter(invoiceDate__lte=date_end)
    result = result.order_by("-invoiceDate")
    paginator = Paginator(result, 20)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'current_filter': {
            'date_start': date_start.strftime("%Y-%m"),
            'date_end': date_end.strftime("%Y-%m")
        }
    }
    return render(request, 'portal/invoices.html', context)


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
        else:
            print(request.POST.get('valid_until'))
            valid_until = datetime.datetime.strptime(request.POST.get('valid_until'), "%Y-%m")
            Billkey(
                orgid=get_organization(request),
                isactive=True,
                billkey="123123",
                alias=request.POST.get("card_alias"),
                auth1=datetime.date.fromisoformat(request.POST.get('owner_birthday')).strftime("%y%m%d"),
                cardno=request.POST.get("card_number"),
                auth2=request.POST.get("card_password"),
                expiremm=valid_until.strftime("%m"),
                expireyy=valid_until.strftime("%y"),
                reguserid=request.user
            ).save()
            card_message = "카드가 등록되었습니다."
    billkeys = Billkey.objects.filter(orgid=get_organization(request))
    return render(request, 'portal/manage_payments.html',
        {'payments': billkeys,
        'card_error': card_error,
        'card_message': card_message})

def search_orgs(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", None)
    if request.user.is_staff:
        result = Organization.objects
    else:
        result = request.user.organizations_organization
    if query is None or query == "":
        result = result.filter(is_active=True).values("name", "slug")[:8]
    else:
        result = result.filter(name__contains=query, is_active=True).values("name", "slug")
    print(list(result))
    return JsonResponse({'result':list(result)})
                  
