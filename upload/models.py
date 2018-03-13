from django.db import models


class File(models.Model):
    """This holds a single user uploaded file"""
    file_field = models.FileField(upload_to='uploads/')
