from django.contrib import admin

from django_file_upload.core.admin import CommonAdmin
from .models import BuyerWiseCon


admin.site.register(BuyerWiseCon, CommonAdmin)
