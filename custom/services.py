from organizations.models import Organization, OrganizationUser
from organizations.backends.defaults import InvitationBackend
from custom.models import User, OrganizationVendor

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

class OrgDirectInvitations(InvitationBackend):
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
                self.send_invitation(user, sender, **kwargs)
                return user