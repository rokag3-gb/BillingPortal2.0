from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.response import TemplateResponse

from Mate365BillingPortal.settings import POLICY_INFO, POLICY_INFO_PROTECTION
from policy.forms import PolicyForm


def _return_policy(request, policy_type, number=None):
    if number is None:
        if policy_type == 'info':
            number = POLICY_INFO['latest']
        elif policy_type == 'info-protection':
            number = POLICY_INFO_PROTECTION['latest']

    try:
        template = get_template(f"policy/{policy_type}-{number}.html")
    except TemplateDoesNotExist:
        raise Http404('해당 버젼의 약관은 존재하지 않습니다.')

    return TemplateResponse(request, template)


def info(request, info_number=None):
    return _return_policy(request=request, policy_type='info', number=info_number)


def info_protection(request, info_protection_number=None):
    return _return_policy(request=request, policy_type='info-protection', number=info_protection_number)


def confirm(request):
    user = request.user

    if request.method == "POST":
        form = PolicyForm(request.POST)
        if form.is_valid():
            user.profile.agree_info(info_number=form.cleaned_data['info_protection'])
            user.profile.agree_info_protection(info_protection_number=form.cleaned_data['info_protection'])
            user.profile.save()
            return redirect('dashboard')
    else:
        form = PolicyForm()

    context = {
        'info': POLICY_INFO,
        'info_protection': POLICY_INFO_PROTECTION,
        'form': form,
    }

    return render(request, f"policy/confirm.html", context=context)
