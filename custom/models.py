from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from organizations.models import Organization, OrganizationUser


class User(AbstractUser):
    org_last_selected = models.ForeignKey(
        Organization, null=True, default=None, blank=True, on_delete=models.SET_DEFAULT)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', primary_key=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, blank=True)
    location = models.CharField(max_length=64, blank=True)


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
