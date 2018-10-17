from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'django_file_upload.core'

    def ready(self):
        from .signals import fire_tasks
