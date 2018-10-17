from django.apps import AppConfig


class UploadConfig(AppConfig):
    name = 'django_file_upload.upload'

    def ready(self):
        from .signals import (post_save_input_file)

