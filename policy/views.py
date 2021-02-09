from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.response import TemplateResponse

from Mate365BillingPortal.settings import POLICY_TERMS_OF_USE, POLICY_INFO_PROTECTION, POLICY_USING_CREDIT_CARD
from policy.forms import PolicyForm

TYPE_TERMS_OF_USE = 'terms-of-use'
TYPE_INFO_GATHERING = 'info-gathering'
TYPE_INFO_USING_CREDIT_CARD = 'using-credit-card'
POLICIES = {
    TYPE_TERMS_OF_USE: POLICY_TERMS_OF_USE,
    TYPE_INFO_GATHERING: POLICY_INFO_PROTECTION,
    TYPE_INFO_USING_CREDIT_CARD: POLICY_USING_CREDIT_CARD,
}


def _return_policy(request, policy_type, number=None):
    if policy_type not in POLICIES:
        Http404('관련 약관이 존재하지 않습니다.')

    if number is None:
        number = POLICIES[policy_type]['latest']

    try:
        template = get_template(f"policy/{policy_type}-{number}.html")
    except TemplateDoesNotExist:
        raise Http404('해당 버젼의 약관은 존재하지 않습니다.')

    return TemplateResponse(request, template)


def terms_of_use(request, number=None):
    return _return_policy(request=request, policy_type=TYPE_TERMS_OF_USE, number=number)


def info_gathering(request, number=None):
    return _return_policy(request=request, policy_type=TYPE_INFO_GATHERING, number=number)


def using_credit_card(request, number=None):
    return _return_policy(request=request, policy_type=TYPE_INFO_USING_CREDIT_CARD, number=number)


def confirm(request):
    user = request.user

    if request.method == "POST":
        form = PolicyForm(request.POST)
        if form.is_valid():
            user.profile.agree_terms_of_use(number=form.cleaned_data['terms_of_use'])
            user.profile.agree_info_gathering(number=form.cleaned_data['info_gathering'])

            if form.cleaned_data['using_credit_card']:
                user.profile.agree_using_credit_card(number=form.cleaned_data['using_credit_card'])

            return redirect('dashboard')
    else:
        form = PolicyForm()

    context = {
        'terms_of_use': POLICY_TERMS_OF_USE,
        'info_gathering': POLICY_INFO_PROTECTION,
        'using_credit_card': POLICY_USING_CREDIT_CARD,
        'form': form,
    }

    return render(request, f"policy/confirm.html", context=context)
