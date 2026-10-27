from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase
from utilisateur.models import Practitioner
from patient.models import Patient
from organization_location.models import Location

# Create your models here.
class Encounter(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    One episode of care (the spine of the hospital stay).
    Strongly versioned for key attributes and status.
    """
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("arrived", "Arrived"),
        ("in-progress", "In Progress"),
        ("on-leave", "On Leave"),
        ("finished", "Finished"),
        ("cancelled", "Cancelled"),
        ("entered-in-error", "Entered in Error"),
    ]

    CLASS_CHOICES = [
        ("IMP", "Inpatient"),
        ("EMER", "Emergency"),
        ("AMB", "Ambulatory"),
        ("VR", "Virtual"),
        ("HH", "Home Health"),
        ("OBSENC", "Observation"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="encounters"
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="planned")
    class_code = models.CharField(max_length=16, choices=CLASS_CHOICES)

    # Timing
    planned_start = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    # Reason & priority
    reason_text = models.TextField(blank=True)
    priority = models.CharField(max_length=32, blank=True)

    # Hospitalization (mainly inpatient)
    admit_source = models.CharField(max_length=64, blank=True)
    discharge_disposition = models.CharField(max_length=64, blank=True)

    service_type = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "encounter"
        indexes = [
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["start_at"]),
            models.Index(fields=["class_code", "status"]),
        ]


class EncounterLocation(UUIDPrimaryKeyModel, TimeStampedModel):
    """Where the patient was during the Encounter (supports transfers)."""
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name="locations"
    )
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="encounter_stays"
    )
    status = models.CharField(max_length=32, default="active")  # planned, active, completed
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "encounter_location"
        indexes = [
            models.Index(fields=["encounter", "start_at"]),
            models.Index(fields=["location", "start_at"]),
        ]


class EncounterParticipant(UUIDPrimaryKeyModel, TimeStampedModel):
    """Who participated in the Encounter and in what role."""
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name="participants"
    )
    practitioner = models.ForeignKey(
        Practitioner, on_delete=models.PROTECT, related_name="encounter_participations"
    )
    role = models.CharField(max_length=64)  # attending, admitting, consulting, nurse...
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "encounter_participant"
        

