from django.contrib import admin

from django_file_upload.core.admin import CommonAdmin
from .models import MachineDay, SAH, Pcs, GGPcs


admin.site.register(MachineDay, CommonAdmin)
admin.site.register(SAH, CommonAdmin)
admin.site.register(Pcs, CommonAdmin)
admin.site.register(GGPcs, CommonAdmin)
