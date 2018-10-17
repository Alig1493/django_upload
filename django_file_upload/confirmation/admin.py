from django.contrib import admin

from django_file_upload.core.admin import CommonAdmin
from .models import BuyerWise


admin.site.register(BuyerWise, CommonAdmin)
