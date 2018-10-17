from django.apps import AppConfig


class ConfirmationConfig(AppConfig):
    name = 'django_file_upload.confirmation'

    def ready(self):
        from .signals import buyer_wise_calc
