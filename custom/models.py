from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from organizations.models import Organization, OrganizationUser

from Mate365BillingPortal.settings import POLICY_INFO, POLICY_INFO_PROTECTION
from policy.models import PolicyInfoExpired, PolicyInfoProtectionExpired


class User(AbstractUser):
    all_policy_checked = None
    org_last_selected = models.ForeignKey(
        Organization, null=True, default=None, blank=True, on_delete=models.SET_DEFAULT)

    def check_all_policy(self):
        if self.is_staff:
            self.all_policy_checked = True
            return True

        if self.profile.info not in POLICY_INFO['able']:
            raise PolicyInfoExpired

        if self.profile.info_protection not in POLICY_INFO_PROTECTION['able']:
            raise PolicyInfoProtectionExpired

        self.all_policy_checked = True
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', primary_key=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, blank=True)
    location = models.CharField(max_length=64, blank=True)
    info = models.CharField('동의한 이용약관', max_length=16, null=True, default=None, blank=True)
    info_updated_at = models.DateTimeField('이용약관 동의 시간', null=True, default=None, blank=True)
    info_protection = models.CharField('동의한 개인정보보호', max_length=16, null=True, default=None, blank=True)
    info_protection_updated_at = models.DateTimeField('개인정보보호 동의 시간', null=True, default=None, blank=True)

    def agree_info(self, info_number):
        latest_info = POLICY_INFO['latest']

        if POLICY_INFO['latest'] != info_number:
            raise ValueError('유효하지 않은 동의 약관 입니다.')

        self.info = info_number
        self.info_updated_at = timezone.now()

    def agree_info_protection(self, info_protection_number):
        latest_info_protection = POLICY_INFO['latest']

        if POLICY_INFO_PROTECTION['latest'] != latest_info_protection:
            raise ValueError('유효하지 않은 동의 약관 입니다.')

        self.info_protection = info_protection_number
        self.info_protection_updated_at = timezone.now()


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