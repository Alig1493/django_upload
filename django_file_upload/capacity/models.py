from django.db import models

from django_file_upload.core.models import UnitSessionTimeStampModel


class MachineDay(UnitSessionTimeStampModel):
    budget = models.FloatField(blank=True, null=True)
    confirmed = models.FloatField(blank=True, null=True)
    reservations = models.FloatField(blank=True, null=True)
    projections = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    confirmed_perc = models.FloatField(blank=True, null=True, verbose_name="Confirmed %")
    reservations_perc = models.FloatField(blank=True, null=True, verbose_name="Reservations %")
    projections_perc = models.FloatField(blank=True, null=True, verbose_name="Projections %")
    total_perc = models.FloatField(blank=True, null=True, verbose_name="Total %")

    class Meta:
        verbose_name = "Capacity Machine Day"
        verbose_name_plural = "Capacity Machine Days"

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"


class SAH(UnitSessionTimeStampModel):
    budget = models.FloatField(blank=True, null=True)
    confirmed = models.FloatField(blank=True, null=True)
    reservations = models.FloatField(blank=True, null=True)
    projections = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    budget_v_plan = models.FloatField(blank=True, null=True, verbose_name="Budget Vs Plan")
    budget_epm = models.FloatField(blank=True, null=True)
    confirmed_epm = models.FloatField(blank=True, null=True)
    budget_fob = models.FloatField(blank=True, null=True)
    confirmed_fob = models.FloatField(blank=True, null=True)
    budget_va = models.FloatField(blank=True, null=True)
    confirmed_va = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Capacity (SAH)"
        verbose_name_plural = "Capacity (SAH)"

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"


class Pcs(UnitSessionTimeStampModel):
    budget = models.FloatField(blank=True, null=True)
    confirmed = models.FloatField(blank=True, null=True)
    reservations = models.FloatField(blank=True, null=True)
    projections = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Capacity (pc)"
        verbose_name_plural = "Capacity (pcs)"

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"


class GGPcs(UnitSessionTimeStampModel):
    confirmed_12 = models.FloatField(blank=True, null=True, verbose_name="Confirmed 12/ 14gg")
    reservations_12 = models.FloatField(blank=True, null=True, verbose_name="Reservations 12/ 14gg")
    projections_12 = models.FloatField(blank=True, null=True, verbose_name="Projections 12/ 14gg")
    open_12 = models.FloatField(blank=True, null=True, verbose_name="Open 12/ 14gg")

    confirmed_7 = models.FloatField(blank=True, null=True, verbose_name="Confirmed 7gg")
    reservations_7 = models.FloatField(blank=True, null=True, verbose_name="Reservations 7gg")
    projections_7 = models.FloatField(blank=True, null=True, verbose_name="Projections 7gg")
    open_7 = models.FloatField(blank=True, null=True, verbose_name="Open 7gg")

    confirmed_5 = models.FloatField(blank=True, null=True, verbose_name="Confirmed 5gg")
    reservations_5 = models.FloatField(blank=True, null=True, verbose_name="Reservations 5gg")
    projections_5 = models.FloatField(blank=True, null=True, verbose_name="Projections 5gg")
    open_5 = models.FloatField(blank=True, null=True, verbose_name="Open 5gg")

    class Meta:
        verbose_name = "Capacity (GG wise Pc)"
        verbose_name_plural = "Capacity (GG wise Pcs)"

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"
