from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_file_upload.core.utils import calc_rate, calc_sum, calc_diff
from .models import MachineDay, SAH


@receiver(pre_save, sender=MachineDay)
def machine_day_calc(sender, instance, **kwargs):
    instance.confirmed_perc = calc_rate(instance.confirmed, instance.budget)
    instance.reservations_perc = calc_rate(instance.reservations, instance.budget)
    instance.projections_perc = calc_rate(instance.projections, instance.budget)
    instance.total_perc = calc_rate(calc_sum(instance.confirmed, instance.reservations, instance.projections),
                                    instance.budget)


@receiver(pre_save, sender=SAH)
def sah_calc(sender, instance, **kwargs):
    instance.budget_v_plan = calc_diff(calc_diff(calc_sum(instance.confirmed,
                                                          instance.reservations,
                                                          instance.projections),
                                                 instance.budget),
                                       instance.open)


