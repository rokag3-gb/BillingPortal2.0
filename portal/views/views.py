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
        date_start = date_end - datetime.timedelta(days=32)
        date_start = date_start.replace(day=1)
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
                  
