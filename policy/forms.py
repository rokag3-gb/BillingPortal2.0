from django import forms
from django.core.exceptions import ValidationError

from Mate365BillingPortal.settings import POLICY_INFO, POLICY_INFO_PROTECTION


class PolicyForm(forms.Form):
    info = forms.CharField(max_length=16)
    info_protection = forms.CharField(max_length=16)
    checked = forms.BooleanField(required=True)

    def clean_info(self):
        info = self.cleaned_data['info']
        if info != POLICY_INFO['latest']:
            raise ValidationError('잘못된 이용약관 요청 입니다.', code='invalid info')

        return info

    def clean_info_protection(self):
        info_protection = self.cleaned_data['info_protection']
        if info_protection != POLICY_INFO_PROTECTION['latest']:
            raise ValidationError('잘못된 개인정보처리방침 요청 입니다.', code='invalid info-protection')

        return info_protection

    def clean_checked(self):
        checked = self.cleaned_data['checked']
        if not checked:
            raise ValidationError('모두 허용에 체그되어 있지 않습니다.', code='unchecked')

        return checked
