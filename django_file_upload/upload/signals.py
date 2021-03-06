from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import File
from .tasks import run_file_upload_tasks


@receiver(post_save, sender=File)
def post_save_input_file(sender, instance, **kwargs):
    if instance.id:
        print(instance)
        print(instance.file_field.name)
        run_file_upload_tasks.delay(file_name=instance.file_field.name, file_date=instance.date)
