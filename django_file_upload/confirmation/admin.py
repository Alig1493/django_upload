from django.contrib import admin

from django_file_upload.core.admin import CommonAdmin
from .models import BuyerWiseCon, BuyerWiseTotal, Buyer


admin.site.register(BuyerWiseCon, CommonAdmin)
admin.site.register(BuyerWiseTotal, CommonAdmin)
admin.site.register(Buyer)
