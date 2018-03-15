import os

from django.db import models
from django.db.models.functions import datetime


def name_file(filename, directory):

    date = datetime.datetime.today()

    filename, ext = os.path.splitext(filename)

    return f"{filename}_{date}{ext}"


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
    file_field = models.FileField(upload_to=uploads_directory_path)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file_field.name)


class FileDownload(models.Model):
    """This holds a single user uploaded file"""
    file_field = models.FileField(upload_to=downloads_directory_path)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file_field.name)
