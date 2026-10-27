from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

# Create your models here.
class CurrentEncounterHistory(ClinicalFindingBase):
    """
    History of the current encounter / history of present illness.
    Free-text heavy but structured enough for later analysis.
    """
    chief_complaint = models.TextField(blank=True)
    history_of_present_illness = models.TextField(blank=True)
    onset = models.CharField(max_length=128, blank=True)
    duration = models.CharField(max_length=128, blank=True)
    course = models.TextField(blank=True)              # evolution
    associated_symptoms = models.TextField(blank=True)
    relieving_factors = models.TextField(blank=True)
    aggravating_factors = models.TextField(blank=True)
    previous_care = models.TextField(blank=True)       # what was already done

    class Meta:
        db_table = "current_encounter_history"
        indexes = [
            models.Index(fields=["encounter"]),
        ]


class CurrentEncounterHistoryHistory(UUIDPrimaryKeyModel):
    """History table for CurrentEncounterHistory."""
    finding = models.ForeignKey(
        CurrentEncounterHistory, on_delete=models.CASCADE, related_name="history_rows"
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
    chief_complaint = models.TextField(blank=True)
    history_of_present_illness = models.TextField(blank=True)
    onset = models.CharField(max_length=128, blank=True)
    duration = models.CharField(max_length=128, blank=True)
    course = models.TextField(blank=True)
    associated_symptoms = models.TextField(blank=True)
    relieving_factors = models.TextField(blank=True)
    aggravating_factors = models.TextField(blank=True)
    previous_care = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "current_encounter_history_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_current_encounter_history_version"
            )
        ]
        

class Antecedents(ClinicalFindingBase):
    """
    Personal and family antecedents.
    Can be updated over the life of the patient; still linked to an encounter when recorded/reviewed.
    """
    personal_medical = models.TextField(blank=True)
    personal_surgical = models.TextField(blank=True)
    personal_other = models.TextField(blank=True)
    family = models.TextField(blank=True)
    social = models.TextField(blank=True)          # lifestyle, occupation, etc.
    allergies_summary = models.TextField(blank=True)  # quick summary (detailed allergies stay in AllergyIntolerance)

    class Meta:
        db_table = "antecedents"
        indexes = [
            models.Index(fields=["patient", "recorded_at"]),
            models.Index(fields=["encounter"]),
        ]


class AntecedentsHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        Antecedents, on_delete=models.CASCADE, related_name="history_rows"
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
    personal_medical = models.TextField(blank=True)
    personal_surgical = models.TextField(blank=True)
    personal_other = models.TextField(blank=True)
    family = models.TextField(blank=True)
    social = models.TextField(blank=True)
    allergies_summary = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "antecedents_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_antecedents_version"
            )
        ]
        
