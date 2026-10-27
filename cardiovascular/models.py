from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

# Create your models here.
class CardiovascularExam(ClinicalFindingBase):
    """Cardiovascular system examination."""

    # Inspection / general
    chest_shape = models.CharField(max_length=64, blank=True)
    visible_pulsations = models.CharField(max_length=128, blank=True)
    edema = models.CharField(max_length=128, blank=True)          # location + severity

    # Palpation
    apex_beat = models.CharField(max_length=128, blank=True)
    thrills = models.CharField(max_length=128, blank=True)
    heave = models.CharField(max_length=64, blank=True)

    # Auscultation
    heart_sounds = models.CharField(max_length=128, blank=True)   # S1, S2, added sounds
    murmurs = models.TextField(blank=True)
    pericardial_rub = models.BooleanField(null=True, blank=True)

    # Peripheral
    peripheral_pulses = models.CharField(max_length=128, blank=True)
    capillary_refill = models.CharField(max_length=64, blank=True)
    jugular_venous_pressure = models.CharField(max_length=64, blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "cardiovascular_exam"


class CardiovascularExamHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        CardiovascularExam, on_delete=models.CASCADE, related_name="history_rows"
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
    edema = models.CharField(max_length=128, blank=True)
    heart_sounds = models.CharField(max_length=128, blank=True)
    murmurs = models.TextField(blank=True)
    peripheral_pulses = models.CharField(max_length=128, blank=True)
    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "cardiovascular_exam_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_cardiovascular_exam_version"
            )
        ]