from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase
from utilisateur.models import Practitioner
from organization_location.models import Location
from patient.models import Patient
from encounter.models import Encounter


class ProcedureOrder(UUIDPrimaryKeyModel, TimeStampedModel):
    pass

# Create your models here.
class Procedure(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    A procedure performed on the patient
    (medical, nursing, surgical, diagnostic...).
    """
    STATUS_CHOICES = [
        ("preparation", "Preparation"),
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
        ("not-done", "Not Done"),
        ("stopped", "Stopped"),
        ("cancelled", "Cancelled"),
        ("entered-in-error", "Entered in Error"),
    ]

    CATEGORY_CHOICES = [
        ("surgical", "Surgical"),
        ("medical", "Medical"),
        ("nursing", "Nursing"),
        ("diagnostic", "Diagnostic"),
        ("other", "Other"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="procedures"
    )
    encounter = models.ForeignKey(
        Encounter, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="procedures"
    )
    order = models.ForeignKey(
        ProcedureOrder, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="procedures"
    )

    # What was done
    code_system = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=64, blank=True)
    code_display = models.CharField(max_length=255, blank=True)
    code_text = models.CharField(max_length=255)  # mandatory free text

    category = models.CharField(
        max_length=32, choices=CATEGORY_CHOICES, default="medical"
    )
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="completed"
    )

    # Timing
    performed_start = models.DateTimeField(null=True, blank=True)
    performed_end = models.DateTimeField(null=True, blank=True)

    # Who
    performer = models.ForeignKey(
        Practitioner, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="performed_procedures"
    )
    location = models.ForeignKey(
        Location, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="procedures"
    )

    reason_text = models.TextField(blank=True)
    outcome = models.TextField(blank=True)          # result / outcome of the procedure
    complication = models.TextField(blank=True)
    note = models.TextField(blank=True)

    # For "not done"
    status_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "procedure"
        indexes = [
            models.Index(fields=["patient", "performed_start"]),
            models.Index(fields=["encounter"]),
            models.Index(fields=["category", "status"]),
        ]


class ProcedureHistory(UUIDPrimaryKeyModel):
    procedure = models.ForeignKey(
        Procedure, on_delete=models.CASCADE, related_name="history_rows"
    )
    version = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    change_type = models.CharField(max_length=32)
    changed_by = models.ForeignKey(
        Practitioner, null=True, blank=True, on_delete=models.SET_NULL
    )
    changed_at = models.DateTimeField()
    change_reason = models.TextField(blank=True)

    status = models.CharField(max_length=32)
    code_text = models.CharField(max_length=255)
    category = models.CharField(max_length=32)
    performed_start = models.DateTimeField(null=True, blank=True)
    performed_end = models.DateTimeField(null=True, blank=True)
    outcome = models.TextField(blank=True)
    complication = models.TextField(blank=True)
    note = models.TextField(blank=True)
    status_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "procedure_history"
        constraints = [
            models.UniqueConstraint(
                fields=["procedure", "version"],
                name="unique_procedure_version"
            )
        ]