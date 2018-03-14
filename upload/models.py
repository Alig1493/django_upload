from django.db import models


class File(models.Model):
    """This holds a single user uploaded file"""
    file_field = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class FileDownload(models.Model):
    """This holds a single user uploaded file"""
    file_field = models.FileField(upload_to='downloads/')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
