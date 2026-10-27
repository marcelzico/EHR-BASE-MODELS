from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from organization_location.models import Organization

class Patient(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Longitudinal patient record.
    Strongly versioned (history table will be added).
    """
    active = models.BooleanField(default=True)

    # Demographics (core)
    family_name = models.CharField(max_length=128)
    given_name = models.CharField(max_length=128, blank=True)
    gender = models.CharField(max_length=16, blank=True)  # male, female, other, unknown
    birth_date = models.DateField(null=True, blank=True)

    deceased = models.BooleanField(default=False)
    deceased_at = models.DateTimeField(null=True, blank=True)

    # Merge support
    merged_into = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="merged_from"
    )

    managing_organization = models.ForeignKey(
        Organization, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="patients"
    )

    class Meta:
        db_table = "patient"
        indexes = [
            models.Index(fields=["family_name", "given_name"]),
            models.Index(fields=["birth_date"]),
        ]


class PatientIdentifier(UUIDPrimaryKeyModel, TimeStampedModel):
    """Business identifiers (MRN, national ID, etc.)."""
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="identifiers"
    )
    system = models.CharField(max_length=255)          # e.g. "urn:hospital:mrn"
    value = models.CharField(max_length=128)
    type_code = models.CharField(max_length=64, blank=True)  # MR, NI, etc.
    assigner = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.SET_NULL
    )
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "patient_identifier"
        indexes = [
            models.Index(fields=["system", "value"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["system", "value"],
                name="unique_patient_identifier_system_value"
            )
        ]