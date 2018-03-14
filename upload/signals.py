from django.db.models.signals import post_save
from django.dispatch import receiver

from upload.models import File
from upload.sq_projected_cap_scraper import process_file


@receiver(post_save, sender=File)
def post_save_input_file(sender, instance, **kwargs):
    if instance.id:
        print(instance.file_field.path)
        process_file(input_file_path=instance.file_field.path)
