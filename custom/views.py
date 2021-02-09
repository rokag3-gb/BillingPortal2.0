from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.urls import reverse
from organizations.models import Organization

from Mate365BillingPortal import settings
from custom.services import set_organization, get_organization


def list_org(request):
    org_list = request.user.organizations_organization.all()

    if len(org_list) == 1:
        return redirect(reverse('switch-to-org', kwargs={'organization_slug': org_list[0].slug}))

    context = {
        'organizations': org_list
    }

    return render(request, 'organizations/list.html', context)


def switch_to_org(request, organization_slug):
    user = request.user
    org = get_object_or_404(Organization, slug=organization_slug)

    if not org.is_member(user=user):
        raise Http404('org 가 없거나, 권한이 없습니다.')

    set_organization(request=request, org=org)

    return redirect(reverse('dashboard'))


class CustomLoginView(LoginView):
    def get_success_url(self):
        org = get_organization(request=self.request)
        # TODO: 만약에 org 를 못 받는 경우가 생기면 안내 메시지 페이지로 연결한다.

        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)
