from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

# Create your models here.
class NeurologicalExam(ClinicalFindingBase):
    """Neurological examination."""

    consciousness_level = models.CharField(max_length=64, blank=True)   # GCS or description
    gcs_eye = models.PositiveSmallIntegerField(null=True, blank=True)
    gcs_verbal = models.PositiveSmallIntegerField(null=True, blank=True)
    gcs_motor = models.PositiveSmallIntegerField(null=True, blank=True)
    gcs_total = models.PositiveSmallIntegerField(null=True, blank=True)

    orientation = models.CharField(max_length=128, blank=True)
    cranial_nerves = models.TextField(blank=True)
    motor_function = models.TextField(blank=True)
    sensory_function = models.TextField(blank=True)
    reflexes = models.TextField(blank=True)
    coordination = models.TextField(blank=True)
    gait = models.CharField(max_length=128, blank=True)
    meningeal_signs = models.CharField(max_length=128, blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "neurological_exam"


class NeurologicalExamHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        NeurologicalExam, on_delete=models.CASCADE, related_name="history_rows"
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
    consciousness_level = models.CharField(max_length=64, blank=True)
    gcs_total = models.PositiveSmallIntegerField(null=True, blank=True)
    cranial_nerves = models.TextField(blank=True)
    motor_function = models.TextField(blank=True)
    sensory_function = models.TextField(blank=True)
    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "neurological_exam_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_neurological_exam_version"
            )
        ]