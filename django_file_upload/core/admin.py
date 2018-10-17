from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from django_file_upload.core.config import ADMIN_EXCLUDE_FIELDS


class CommonAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        exclude_fields = ADMIN_EXCLUDE_FIELDS
        include_fields = [f.name for f in self.model._meta.get_fields() if f.name not in exclude_fields]
        return include_fields


admin.site.unregister(EmailAddress)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(Site)
admin.site.unregister(Group)
