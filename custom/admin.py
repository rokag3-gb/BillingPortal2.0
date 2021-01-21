from django.contrib import admin
from organizations.models import Organization

from custom.models import UserProfile, OrganizationProfile, User


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
    inlines = (OrganizationProfileInline, )


admin.site.unregister(Organization)
admin.site.register(Organization, OrganizationProfileAdmin)
