from django.contrib import admin

# Register your models here.
from .models import File, FileDownload

admin.site.register(File)
admin.site.register(FileDownload)
