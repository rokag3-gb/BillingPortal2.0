from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from organizations.models import Organization, OrganizationUser

from Mate365BillingPortal.settings import POLICY_TERMS_OF_USE, POLICY_INFO_PROTECTION, POLICY_USING_CREDIT_CARD
from policy.models import PolicyTermsOfUse, PolicyInfoGatheringExpired


class User(AbstractUser):
    all_policy_checked = None
    org_last_selected = models.ForeignKey(
        Organization, null=True, default=None, blank=True, on_delete=models.SET_DEFAULT)

    def check_all_policy(self):
        if self.is_staff:
            self.all_policy_checked = True
            return True

        if self.profile.terms_of_use not in POLICY_TERMS_OF_USE['able']:
            raise PolicyTermsOfUse

        if self.profile.info_gathering not in POLICY_INFO_PROTECTION['able']:
            raise PolicyInfoGatheringExpired

        self.all_policy_checked = True
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', primary_key=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, blank=True)
    location = models.CharField(max_length=64, blank=True)
    terms_of_use = models.CharField('동의한 이용약관', max_length=16, null=True, default=None, blank=True)
    terms_of_use_updated_at = models.DateTimeField('이용약관 동의 시간', null=True, default=None, blank=True)
    info_gathering = models.CharField('동의한 개인정보보호', max_length=16, null=True, default=None, blank=True)
    info_gathering_updated_at = models.DateTimeField('개인정보보호 동의 시간', null=True, default=None, blank=True)
    using_credit_card = models.CharField('동의한 신용카드결제 허용', max_length=16, null=True, default=None, blank=True)
    using_credit_card_updated_at = models.DateTimeField('신용카드결제 허용 동의 시간', null=True, default=None, blank=True)

    def agree_terms_of_use(self, number):
        if POLICY_TERMS_OF_USE['latest'] != number:
            raise ValueError('유효하지 않은 약관 동의 입니다.')

        self.terms_of_use = number
        self.terms_of_use_updated_at = timezone.now()
        self.save()

    def agree_info_gathering(self, number):
        if POLICY_INFO_PROTECTION['latest'] != number:
            raise ValueError('유효하지 않은 약관 동의 입니다.')

        self.info_gathering = number
        self.info_gathering_updated_at = timezone.now()
        self.save()

    def agree_using_credit_card(self, number):
        if POLICY_USING_CREDIT_CARD['latest'] != number:
            raise ValueError('유효하지 않은 약관 동의 입니다.')

        self.using_credit_card = number
        self.using_credit_card_updated_at = timezone.now()
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class OrganizationProfile(models.Model):
    org = models.OneToOneField(Organization, related_name='profile', primary_key=True, on_delete=models.CASCADE)
    company_registration_number = models.CharField('사업자번호', max_length=16, blank=True)
    location = models.CharField(max_length=64, blank=True)


@receiver(post_save, sender=Organization)
def create_organization_profile(sender, instance, created, **kwargs):
    if created:
        OrganizationProfile.objects.create(org=instance)


@receiver(post_save, sender=Organization)
def save_organization_profile(sender, instance, **kwargs):
    instance.profile.save()


class Org(Organization):
    class Meta:
        proxy = True

class OrgUser(OrganizationUser):
    class Meta:
        proxy = True

class OrganizationVendor(models.Model):
    class VendorCode(models.IntegerChoices):
       AWS = 1, "Amazon Web Services"
       AZURE = 2, "Microsoft Azure"
       GCP = 3, "Google Cloud Platform"
    class Meta:
        managed = False
        db_table = 'Organization_Vendor'
        verbose_name = "조직별 클라우드 연결"
        verbose_name_plural = "조직별 클라우드 연결"
    seq = models.AutoField(db_column='Seq', primary_key=True, verbose_name='순번')  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='OrgId', verbose_name='조직')  # Field name made lowercase.
    vendorcode = models.IntegerField(db_column='VendorCode', choices=VendorCode.choices, verbose_name='클라우드 공급자')  # Field name made lowercase.
    vendorkey = models.CharField(db_column='VendorKey', max_length=200, verbose_name='벤더 키(테넌트ID, 구독ID 등)')  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate', verbose_name='등록일시', auto_now_add=True)  # Field name made lowercase.

class Invoice(models.Model):
    invoiceId = models.CharField(max_length=57, db_column="InvoiceId", primary_key=True)
    invoiceMonth = models.CharField(max_length=6, db_column="InvoiceMonth")
    invoiceDate = models.DateField(db_column="InvoiceDate")
    tenantId = models.CharField(max_length=4, db_column="TenantId")
    subscriptionId = models.CharField(max_length=50, db_column="SubscriptionId")
    subscriptionName = models.CharField(max_length=4000, db_column="SubscriptionName")
    chargeStartDate = models.DateField(db_column="ChargeStartDate")
    chargeEndDate = models.DateField(db_column="ChargeEndDate")
    subTotal = models.FloatField(db_column="SubTotal")
    subTotalRrp = models.FloatField(db_column="SubTotalRrp")
    datetimeStamp = models.DateTimeField(db_column="datetime_stamp")
    class Meta:
        managed = False
        db_table = "VW_AzureRhipe_invoice"