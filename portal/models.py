from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=20, default="orgname", verbose_name="조직 이름")
    desc = models.TextField(default="", verbose_name="조직 소개")
    members = models.ManyToManyField(User, through='Membership', verbose_name="회원")

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    joined_at = models.DateTimeField()
