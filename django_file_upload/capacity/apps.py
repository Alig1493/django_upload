from django.apps import AppConfig


class CapacityConfig(AppConfig):
    name = 'django_file_upload.capacity'

    def ready(self):
        from .signals import machine_day_calc, sah_calc
