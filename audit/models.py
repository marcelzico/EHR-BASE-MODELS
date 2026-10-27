from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase
from utilisateur.models import Practitioner
from encounter.models import Encounter

# Create your models here.
class AuditEvent(UUIDPrimaryKeyModel):
    """Append-only audit log."""
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)
    actor = models.ForeignKey(
        Practitioner, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="audit_events"
    )
    action = models.CharField(max_length=64)          # create, update, status_change, delete...
    entity_type = models.CharField(max_length=64)     # Patient, Encounter, ...
    entity_id = models.UUIDField()
    outcome = models.CharField(max_length=32, default="success")
    reason = models.TextField(blank=True)
    extra = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "audit_event"
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["occurred_at"]),
        ]
        


class EncounterHistory(UUIDPrimaryKeyModel):
    """Previous versions of key Encounter attributes + status."""
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name="history_rows"
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

    # Snapshot
    status = models.CharField(max_length=32)
    class_code = models.CharField(max_length=16)
    planned_start = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    reason_text = models.TextField(blank=True)
    priority = models.CharField(max_length=32, blank=True)
    admit_source = models.CharField(max_length=64, blank=True)
    discharge_disposition = models.CharField(max_length=64, blank=True)
    service_type = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "encounter_history"
        indexes = [
            models.Index(fields=["encounter", "version"]),
            models.Index(fields=["encounter", "valid_from", "valid_to"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["encounter", "version"],
                name="unique_encounter_version"
            )
        ]