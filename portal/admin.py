from django.contrib import admin
from .models import Organization, Membership

# Register your models here.
@admin.register(Organization, Membership)
class OrgAdmin(admin.ModelAdmin):
    pass

