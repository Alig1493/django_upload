import os

from django.conf import settings
from django.db import models


def name_file(filename, directory):

    number = len(os.listdir(f"{settings.MEDIA_ROOT}/{directory}"))
    filename, ext = os.path.splitext(filename)

    if number:
        return f"{filename}_{number}{ext}"
    return f"{filename}{ext}"


def uploads_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/<filename>
    filename = name_file(filename=filename, directory='uploads')
    return f"uploads/{filename}"


def downloads_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/downloads/<filename>
    filename = name_file(filename=filename, directory='downloads')
    return f"downloads/{filename}"


class File(models.Model):
    """This holds a single user uploaded file"""
    file_field = models.FileField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file_field.name)


class FileDownload(models.Model):
    """This holds a single user uploaded file"""
    file_field = models.FileField(upload_to="downloads/")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file_field.name)
