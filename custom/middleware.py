from django.contrib.auth.middleware import get_user
from django.shortcuts import redirect
from django.urls import reverse

from policy.models import PolicyTermsOfUse, PolicyInfoGatheringExpired


def policy_check_middleware(get_response):
    none_check_pages = (
        reverse('login'),
        reverse('logout'),
        reverse('confirm'),
        reverse('terms-of-use-latest'), reverse('info-gathering-latest'), reverse('using-credit-card-latest'),
    )

    def middleware(request):
        if request.path in none_check_pages:
            return get_response(request)

        user = get_user(request=request)

        if user.is_anonymous:
            return get_response(request)

        try:
            if user.all_policy_checked is None:
                user.check_all_policy()

        except (PolicyTermsOfUse, PolicyInfoGatheringExpired) as e:
            return redirect('confirm')

        if user.all_policy_checked:
            return get_response(request)

        # TODO: 만약 약관 또는 개인정보처리방침이 갱신이 되었지만 사용가능하다면, message 로 알림을 전달하기
        return get_response(request)

    return middleware
