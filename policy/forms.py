from django import forms
from django.core.exceptions import ValidationError

from Mate365BillingPortal.settings import POLICY_TERMS_OF_USE, POLICY_INFO_PROTECTION, POLICY_USING_CREDIT_CARD


class PolicyForm(forms.Form):
    terms_of_use = forms.CharField(max_length=16, required=True)
    info_gathering = forms.CharField(max_length=16, required=True)
    using_credit_card = forms.CharField(max_length=16, required=False)

    def clean_terms_of_use(self):
        terms_of_use = self.cleaned_data['terms_of_use']
        if terms_of_use != POLICY_TERMS_OF_USE['latest']:
            raise ValidationError('잘못된 이용약관 요청 입니다.', code='invalid Terms Of Use')

        return terms_of_use

    def clean_info_gathering(self):
        info_gathering = self.cleaned_data['info_gathering']
        if info_gathering != POLICY_INFO_PROTECTION['latest']:
            raise ValidationError('잘못된 개인정보처리방침 요청 입니다.', code='invalid Info Gathering')

        return info_gathering

    def clean_using_credit_card(self):
        using_credit_card = self.cleaned_data['using_credit_card']

        # INFO: BooleanField 를 CharField 로 강제로 쓰면서 처리할 부분
        if using_credit_card == '':
            return None

        if using_credit_card != POLICY_USING_CREDIT_CARD['latest']:
            raise ValidationError('잘못된 신용카드 처리 허용 요청 입니다.', code='invalid credit card')

        return using_credit_card
