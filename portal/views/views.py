import datetime

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from custom.services import get_organization
from custom.models import Invoice, UserProfile, Organization, OrgUser
from organizations.backends import invitation_backend


def index(request: HttpRequest) -> HttpResponse:
    # return render(request, 'portal/index.html')
    return redirect('/dashboard')


@login_required
def preference(request: HttpRequest) -> HttpResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    context = {"user_profile":user_profile}
    if request.method == "POST":
        if request.user.check_password(request.POST.get("user_confirm_password", "")):
            user_profile.phone = request.POST.get("user_billing_phone", "")
            user_profile.location = request.POST.get("user_billing_addr", "")
            user_profile.save()
            context["result"] = "수정된 개인정보가 저장되었습니다."
        else:
            context["error"] = "로그인 암호가 틀려서 수정된 개인정보가 저장되지 않았습니다."
    return render(request, 'portal/settings/index.html', context)

def orgsettings(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        user_email = request.POST.get("new_user_email", None)
        if user_email is None:
            context["error"] = "새로 초대할 사람의 이메일을 입력하세요."
        else:
            invitation_backend().invite_by_email(user_email, sender=request.user, request=request)
            context["result"] = "{}로 회원 가입 및 조직 초대 메일이 발송되었습니다.".format(user_email)
    context["members"] = OrgUser.objects.filter(organization=get_organization(request))
    return render(request, 'portal/settings/org.html', context)

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
                  
