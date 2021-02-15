from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from organizations.models import Organization, OrganizationUser
from typing import List

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

    def can_use_create_card(self):
        if self.profile.using_credit_card in POLICY_USING_CREDIT_CARD['able']:
            return True

        return False


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
    seq = models.AutoField(db_column='Seq', primary_key=True)  # Field name made lowercase.
    invoiceMonth = models.CharField(db_column='InvoiceMonth', max_length=6)  # Field name made lowercase.
    invoiceDate = models.DateField(db_column='InvoiceDate')
    invoiceId = models.CharField(db_column='InvoiceId', unique=True, max_length=13, blank=True, null=True)  # Field name made lowercase.
    orgId = models.ForeignKey(Organization, models.DO_NOTHING, db_column='OrgId')  # Field name made lowercase.
    orgKey = models.CharField(db_column='OrgKey', max_length=7)  # Field name made lowercase.
    orgName = models.CharField(db_column='OrgName', max_length=200)
    vendorCode = models.CharField(db_column='VendorCode', max_length=7)  # Field name made lowercase.
    vendorName = models.CharField(db_column='VendorName', max_length=200)
    vendorInvoiceId = models.CharField(db_column='VendorInvoiceId', max_length=100)  # Field name made lowercase.
    chargeStartDate = models.DateField(db_column='ChargeStartDate')  # Field name made lowercase.
    chargeEndDate = models.DateField(db_column='ChargeEndDate')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    amountRrp = models.DecimalField(db_column='AmountRrp', max_digits=19, decimal_places=4)  # Field name made lowercase.
    regId = models.IntegerField(db_column='RegId')  # Field name made lowercase.
    regDate = models.DateTimeField(db_column='RegDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VW_Invoice'
        # unique_together = (('invoicemonth', 'orgid', 'vendorcode', 'vendorinvoiceid'),)

class InvoiceOrder(models.Model):
    orderNo = models.AutoField(db_column='OrderNo', primary_key=True)  # Field name made lowercase.
    orderDate = models.DateField(db_column='OrderDate')  # Field name made lowercase.
    orderUserId = models.ForeignKey(User, models.DO_NOTHING, db_column='OrderUserId')  # Field name made lowercase.
    orgId = models.ForeignKey(Organization, models.DO_NOTHING, db_column='OrgId')  # Field name made lowercase.
    totalAmount = models.DecimalField(db_column='TotalAmount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    paid = models.DecimalField(db_column='Paid', max_digits=19, decimal_places=4)  # Field name made lowercase.
    isCancel = models.BooleanField(db_column='IsCancel')  # Field name made lowercase.
    regDate = models.DateTimeField(db_column='RegDate', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InvoiceOrder'
    
    def createDetails(self, orderDetails: List[Invoice]):
        for item in orderDetails:
            detail = InvoiceOrderDetail(
                orderNo = self,
                invoiceDate = item.invoiceDate,
                invoiceMonth = item.invoiceMonth,
                vendorCode = item.vendorCode,
                invoiceId = item.invoiceId,
                amount = item.amountRrp,
                paid = 0
            )
            detail.save()


class InvoiceOrderDetail(models.Model):
    seq = models.AutoField(db_column='Seq', primary_key=True)  # Field name made lowercase.
    orderNo = models.ForeignKey(InvoiceOrder, models.DO_NOTHING, db_column='OrderNo')  # Field name made lowercase.
    invoiceDate = models.DateField(db_column='InvoiceDate')  # Field name made lowercase.
    invoiceMonth = models.CharField(db_column='InvoiceMonth', max_length=6, blank=True, null=True)  # Field name made lowercase.
    vendorCode = models.CharField(db_column='VendorCode', max_length=7)  # Field name made lowercase.
    invoiceId = models.CharField(db_column='InvoiceId', max_length=100)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    paid = models.DecimalField(db_column='Paid', max_digits=19, decimal_places=4)  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InvoiceOrderDetail'

# 결제수단 등록 테이블
class Billkey(models.Model):
    seq = models.AutoField(db_column='Seq', primary_key=True)  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, db_column='OrgId')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    billkey = models.CharField(db_column='Billkey', max_length=500)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=100)  # Field name made lowercase.
    auth1 = models.CharField(db_column='Auth1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardno = models.CharField(db_column='CardNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    auth2 = models.CharField(db_column='Auth2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    expiremm = models.CharField(db_column='ExpireMM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    expireyy = models.CharField(db_column='ExpireYY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reguserid = models.ForeignKey(User, db_column='RegUserId')  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Billkey'