from django.db.models.signals import post_save
from django.dispatch import receiver

from django_file_upload.capacity.models import SAH, MachineDay, Pcs, GGPcs
from django_file_upload.core.utils import chain_reaction


@receiver(post_save, sender=MachineDay)
@receiver(post_save, sender=SAH)
@receiver(post_save, sender=Pcs)
@receiver(post_save, sender=GGPcs)
def fire_tasks(sender, instance, **kwargs):
    month = instance.session
    unit = instance.unit

    if month <= 12 and unit < 2:
        chain_reaction(sender, instance.session, instance.year, instance.unit)
