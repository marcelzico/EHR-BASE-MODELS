from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel

# Create your models here.
class ClinicalFindingBase(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Abstract base for all structured clinical findings / examinations.
    Provides common identity, context, lifecycle and audit hooks.
    """
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("final", "Final"),
        ("amended", "Amended"),
        ("entered-in-error", "Entered in Error"),
    ]

    patient = models.ForeignKey(
        "Patient", on_delete=models.PROTECT, related_name="%(class)s_findings"
    )
    encounter = models.ForeignKey(
        "Encounter", on_delete=models.PROTECT, related_name="%(class)s_findings"
    )

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="draft"
    )
    recorded_at = models.DateTimeField()
    recorded_by = models.ForeignKey(
        "Practitioner", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="%(class)s_recorded"
    )

    note = models.TextField(blank=True)

    class Meta:
        abstract = True
        
        
class VitalSigns(ClinicalFindingBase):
    """Core vital signs recorded during an encounter."""

    temperature_c = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    heart_rate = models.PositiveSmallIntegerField(null=True, blank=True)          # bpm
    respiratory_rate = models.PositiveSmallIntegerField(null=True, blank=True)    # /min
    blood_pressure_systolic = models.PositiveSmallIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveSmallIntegerField(null=True, blank=True)
    oxygen_saturation = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # %
    pain_score = models.PositiveSmallIntegerField(null=True, blank=True)          # 0-10
    consciousness = models.CharField(max_length=64, blank=True)                   # alert, voice, pain, unresponsive...

    # Optional context
    position = models.CharField(max_length=64, blank=True)        # sitting, lying...
    oxygen_therapy = models.CharField(max_length=64, blank=True)  # room air, nasal cannula...

    class Meta:
        db_table = "vital_signs"
        indexes = [
            models.Index(fields=["encounter", "recorded_at"]),
            models.Index(fields=["patient", "recorded_at"]),
        ]


class VitalSignsHistory(UUIDPrimaryKeyModel):
    vital_signs = models.ForeignKey(
        VitalSigns, on_delete=models.CASCADE, related_name="history_rows"
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

    # Snapshot of main fields
    status = models.CharField(max_length=32)
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    heart_rate = models.PositiveSmallIntegerField(null=True, blank=True)
    respiratory_rate = models.PositiveSmallIntegerField(null=True, blank=True)
    blood_pressure_systolic = models.PositiveSmallIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveSmallIntegerField(null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pain_score = models.PositiveSmallIntegerField(null=True, blank=True)
    consciousness = models.CharField(max_length=64, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "vital_signs_history"
        constraints = [
            models.UniqueConstraint(
                fields=["vital_signs", "version"],
                name="unique_vital_signs_version"
            )
        ]
        

class GeneralExamination(ClinicalFindingBase):
    """
    General physical examination / overall clinical state.
    Usually performed at the beginning of the clinical assessment.
    """
    general_appearance = models.TextField(blank=True)          # well/ill-looking, distress...
    consciousness = models.CharField(max_length=64, blank=True)
    nutritional_status = models.CharField(max_length=64, blank=True)
    hydration = models.CharField(max_length=64, blank=True)
    colour = models.CharField(max_length=64, blank=True)       # pallor, jaundice, cyanosis...
    oedema = models.CharField(max_length=128, blank=True)
    lymphadenopathy = models.CharField(max_length=128, blank=True)
    temperature_feeling = models.CharField(max_length=64, blank=True)  # febrile, cold...
    posture_gait = models.CharField(max_length=128, blank=True)
    hygiene = models.CharField(max_length=64, blank=True)
    other_signs = models.TextField(blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "general_examination"
        indexes = [
            models.Index(fields=["encounter", "recorded_at"]),
        ]


class GeneralExaminationHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        GeneralExamination, on_delete=models.CASCADE, related_name="history_rows"
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
    general_appearance = models.TextField(blank=True)
    consciousness = models.CharField(max_length=64, blank=True)
    nutritional_status = models.CharField(max_length=64, blank=True)
    hydration = models.CharField(max_length=64, blank=True)
    colour = models.CharField(max_length=64, blank=True)
    oedema = models.CharField(max_length=128, blank=True)
    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "general_examination_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_general_examination_version"
            )
        ]
        
