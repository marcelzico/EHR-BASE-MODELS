from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase
from encounter.models import Encounter
from utilisateur.models import Practitioner
from patient.models import Patient

# Create your models here.
class MedicationRequest(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Prescription / medication order.
    """
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("on-hold", "On Hold"),
        ("completed", "Completed"),
        ("stopped", "Stopped"),
        ("cancelled", "Cancelled"),
        ("entered-in-error", "Entered in Error"),
    ]

    INTENT_CHOICES = [
        ("order", "Order"),
        ("plan", "Plan"),
    ]

    CATEGORY_CHOICES = [
        ("inpatient", "Inpatient"),
        ("outpatient", "Outpatient"),
        ("community", "Community"),
        ("discharge", "Discharge"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="medication_requests"
    )
    encounter = models.ForeignKey(
        Encounter, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="medication_requests"
    )

    # Medication
    medication_code_system = models.CharField(max_length=255, blank=True)
    medication_code = models.CharField(max_length=64, blank=True)
    medication_display = models.CharField(max_length=255, blank=True)
    medication_text = models.CharField(max_length=255)  # required free-text name

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="active"
    )
    intent = models.CharField(
        max_length=32, choices=INTENT_CHOICES, default="order"
    )
    category = models.CharField(
        max_length=32, choices=CATEGORY_CHOICES, blank=True
    )

    # Dosage
    dose_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    dose_unit = models.CharField(max_length=32, blank=True)
    route = models.CharField(max_length=64, blank=True)          # oral, IV, IM...
    frequency = models.CharField(max_length=128, blank=True)     # e.g. "3 times a day"
    duration_text = models.CharField(max_length=128, blank=True) # e.g. "for 7 days"
    additional_instruction = models.TextField(blank=True)

    # Authorship
    requester = models.ForeignKey(
        Practitioner, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="prescribed_medications"
    )
    authored_at = models.DateTimeField(null=True, blank=True)

    reason_text = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "medication_request"
        indexes = [
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["encounter"]),
            models.Index(fields=["authored_at"]),
        ]


class MedicationRequestHistory(UUIDPrimaryKeyModel):
    medication_request = models.ForeignKey(
        MedicationRequest, on_delete=models.CASCADE, related_name="history_rows"
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
    medication_text = models.CharField(max_length=255)
    dose_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dose_unit = models.CharField(max_length=32, blank=True)
    route = models.CharField(max_length=64, blank=True)
    frequency = models.CharField(max_length=128, blank=True)
    duration_text = models.CharField(max_length=128, blank=True)
    additional_instruction = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "medication_request_history"
        constraints = [
            models.UniqueConstraint(
                fields=["medication_request", "version"],
                name="unique_medication_request_version"
            )
        ]
        
        

class MedicationDispense(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    What was actually dispensed by the pharmacy.
    """
    STATUS_CHOICES = [
        ("preparation", "Preparation"),
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("entered-in-error", "Entered in Error"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="medication_dispenses"
    )
    medication_request = models.ForeignKey(
        MedicationRequest, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="dispenses"
    )
    encounter = models.ForeignKey(
        Encounter, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="medication_dispenses"
    )

    medication_text = models.CharField(max_length=255)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="completed"
    )

    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    quantity_unit = models.CharField(max_length=32, blank=True)
    days_supply = models.PositiveSmallIntegerField(null=True, blank=True)

    when_prepared = models.DateTimeField(null=True, blank=True)
    when_handed_over = models.DateTimeField(null=True, blank=True)

    dispenser = models.ForeignKey(
        Practitioner, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="dispensed_medications"
    )
    note = models.TextField(blank=True)

    class Meta:
        db_table = "medication_dispense"
        indexes = [
            models.Index(fields=["patient", "when_handed_over"]),
            models.Index(fields=["medication_request"]),
        ]
        
        
