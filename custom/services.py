from organizations.models import Organization, OrganizationUser
from organizations.backends.defaults import InvitationBackend
from custom.models import User, OrganizationVendor
from organizations.backends.forms import UserRegistrationForm
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect


SESSION_ORGANIZATION = 'S_ORG'


def _choice_one_org(user: User):
    for org_user in OrganizationUser.objects.filter(user=user).order_by('id'):
        org = org_user.organization
        if not org.is_active:
            continue

        return org

    return None


def get_organization(request):
    # INFO: 사용자 DB 에서 저장되어 있는 마지막 org 선택을 기본으로 한다.
    # INFO: 만약에 없다면 다음 org 선택을 자동으로 한다.
    try:
        org = Organization.objects.get(slug=request.session[SESSION_ORGANIZATION], is_active=True)
        if not request.user.is_staff:
            org_user = OrganizationUser.objects.get(user=request.user, organization=org)
        return org
    # INFO: 한번도 로그인 하지 않았다면
    except KeyError:
        pass
    # INFO: org 권한이 사라졌거나
    except OrganizationUser.DoesNotExist:
        pass
    # INFO: org 가 삭제 되었거나 in_active 되었다면
    except Organization.DoesNotExist:
        pass

    org = _choice_one_org(user=request.user)
    set_organization(request=request, org=org)
    return org


def set_organization(request, org):
    request.session[SESSION_ORGANIZATION] = org.slug
    user = request.user

    if user.org_last_selected != org:
        user.org_last_selected = org
        user.save()

def vendors(self):
    return OrganizationVendor.objects.filter(orgid=self)

Organization.add_to_class("vendors", vendors)

class RegistrationForm(UserRegistrationForm):
    """
    Form class that allows a user to register after clicking through an
    invitation.
    """
    username = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(max_length=30, label="이름", widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "이름"}))
    last_name = forms.CharField(max_length=30, label="성", widget=forms.TextInput(attrs={"class":"form-control",  "placeholder": "성"}))
    email = forms.EmailField(widget=forms.HiddenInput())
    # password1 = forms.CharField(widget=forms.HiddenInput())
    # password2 = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control",  "placeholder": "새 암호"}))
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control" , "placeholder": "새 암호 확인"}))

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2 or not password1:
            raise forms.ValidationError("입력한 암호가 일치하지 않습니다.")
        print(self.cleaned_data)
        return super(RegistrationForm, self).clean()

class OrgDirectInvitations(InvitationBackend):
    invitation_subject = 'email/invitation_subject.txt'
    invitation_body = 'email/invitation_body.html'
    reminder_subject = 'email/reminder_subject.txt'
    reminder_body = 'email/reminder_body.html'
    registration_form_template = "registration/invite_register.html"
    activation_success_template = "registration/register_success.html"
    form_class = RegistrationForm

    def invite_by_email(self, email, sender=None, request=None, **kwargs):
        if request is None:
            return None
        else:
            org = get_organization(request)
            if org is None:
                return None
            else:
                try:
                    user = self.user_model.objects.get(email=email)
                    try:
                        OrganizationUser.objects.get(user=user, organization=org)
                    except OrganizationUser.DoesNotExist:
                        org_user = OrganizationUser.objects.create(
                            user=user,
                            organization=org
                        )
                        org_user.save()
                except self.user_model.DoesNotExist:
                    user = self.user_model.objects.create(
                            username=email,
                            email=email,
                            password=self.user_model.objects.make_random_password())
                    user.is_active = False
                    user.save()
                    org_user = OrganizationUser.objects.create(
                            user=user,
                            organization=org
                        )
                    org_user.save()
                self.send_invitation(user, sender, organization=org, baseurl=getattr(settings, "BASE_URL", ""))
                return user
    def activate_view(self, request, user_id, token):
        """
        View function that activates the given User by setting `is_active` to
        true if the provided information is verified.
        """
        try:
            user = self.user_model.objects.get(id=user_id, is_active=False)
        except self.user_model.DoesNotExist:
            raise render(request, self.registration_form_template, {"url_error": True})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise render(request, self.registration_form_template, {"url_error": True})
        form = self.get_form(
            data=request.POST or None, files=request.FILES or None, instance=user
        )
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data["password1"])
            user.save()
            self.activate_organizations(user)
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect(self.get_success_url())
        return render(request, self.registration_form_template, {"form": form})