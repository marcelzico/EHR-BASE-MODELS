from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

# Create your models here.
class GynecologicHistory(ClinicalFindingBase):
    """Gynecologic history (mainly for female patients)."""

    menarche_age = models.PositiveSmallIntegerField(null=True, blank=True)
    last_menstrual_period = models.DateField(null=True, blank=True)
    cycle_regular = models.BooleanField(null=True, blank=True)
    cycle_length_days = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_of_flow_days = models.PositiveSmallIntegerField(null=True, blank=True)
    dysmenorrhea = models.BooleanField(null=True, blank=True)
    contraception = models.CharField(max_length=128, blank=True)
    gravidity = models.PositiveSmallIntegerField(null=True, blank=True)
    parity = models.PositiveSmallIntegerField(null=True, blank=True)
    abortions = models.PositiveSmallIntegerField(null=True, blank=True)
    living_children = models.PositiveSmallIntegerField(null=True, blank=True)
    last_delivery_date = models.DateField(null=True, blank=True)
    last_delivery_mode = models.CharField(max_length=64, blank=True)
    menopause = models.BooleanField(null=True, blank=True)
    menopause_age = models.PositiveSmallIntegerField(null=True, blank=True)
    pap_smear_history = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "gynecologic_history"


class GynecologicHistoryHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        GynecologicHistory, on_delete=models.CASCADE, related_name="history_rows"
    )
    version = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    change_type = models.CharField(max_length=32)
    changed_by = models.ForeignKey(
        "Practitioner", null=True, blank=True, on_delete=models.SET_NULL
    )
    changed_at = models.DateTimeField()
    change_reason = models.TextField(blank=True)

    status = models.CharField(max_length=32)
    # Snapshot of main fields (abbreviated for brevity – full copy in real code)
    menarche_age = models.PositiveSmallIntegerField(null=True, blank=True)
    last_menstrual_period = models.DateField(null=True, blank=True)
    gravidity = models.PositiveSmallIntegerField(null=True, blank=True)
    parity = models.PositiveSmallIntegerField(null=True, blank=True)
    contraception = models.CharField(max_length=128, blank=True)
    other = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "gynecologic_history_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_gynecologic_history_version"
            )
        ]