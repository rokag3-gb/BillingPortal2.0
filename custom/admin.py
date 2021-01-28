from django.contrib import admin
from organizations.models import Organization

from custom.models import UserProfile, OrganizationProfile, User, OrganizationVendor


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

    # verbose_name_plural = 'Profile'
    # fk_name = 'user'


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, )


admin.site.register(User, UserProfileAdmin)


class OrganizationProfileInline(admin.StackedInline):
    model = OrganizationProfile
    can_delete = False
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'slug', 'regnumber', 'location']
    inlines = (OrganizationProfileInline, )
    def regnumber(self, obj):
        return OrganizationProfile.objects.get(org=obj).company_registration_number

    def location(self, obj):
        return OrganizationProfile.objects.get(org=obj).location

class OrgVendorAdmin(admin.ModelAdmin):
    model = OrganizationVendor
    list_display = ['seq', 'orgid', 'vendorcode', 'vendorkey', 'regdate']
    list_filter = ['orgid', 'vendorcode']


admin.site.unregister(Organization)
admin.site.register(Organization, OrganizationProfileAdmin)
admin.site.register(OrganizationVendor, OrgVendorAdmin)
