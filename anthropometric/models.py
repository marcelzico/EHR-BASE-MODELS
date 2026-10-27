from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

# Create your models here.
class Anthropometry(ClinicalFindingBase):
    """
    Weight, height, derived measures.
    Supports both adult and pediatric use.
    """
    weight_kg = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    height_cm = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    head_circumference_cm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # mainly pediatric
    muac_cm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # mid-upper arm circumference

    # Derived / calculated (can also be computed on the fly)
    bmi = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    # Pediatric context
    age_at_measurement_months = models.PositiveIntegerField(null=True, blank=True)
    nutritional_status = models.CharField(max_length=64, blank=True)  # normal, underweight...

    class Meta:
        db_table = "anthropometry"
        indexes = [
            models.Index(fields=["encounter", "recorded_at"]),
            models.Index(fields=["patient", "recorded_at"]),
        ]


class AnthropometryHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        Anthropometry, on_delete=models.CASCADE, related_name="history_rows"
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
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    head_circumference_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    muac_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nutritional_status = models.CharField(max_length=64, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "anthropometry_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_anthropometry_version"
            )
        ]
        

class BirthHistory(ClinicalFindingBase):
    """Birth history – important for pediatric patients."""

    place_of_birth = models.CharField(max_length=128, blank=True)
    delivery_mode = models.CharField(max_length=64, blank=True)  # vaginal, cesarean...
    gestational_age_weeks = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_weight_g = models.PositiveIntegerField(null=True, blank=True)
    birth_length_cm = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    head_circumference_at_birth_cm = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    apgar_1min = models.PositiveSmallIntegerField(null=True, blank=True)
    apgar_5min = models.PositiveSmallIntegerField(null=True, blank=True)
    resuscitation = models.BooleanField(null=True, blank=True)
    neonatal_complications = models.TextField(blank=True)
    maternal_complications = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "birth_history"


class BirthHistoryHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        BirthHistory, on_delete=models.CASCADE, related_name="history_rows"
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
    delivery_mode = models.CharField(max_length=64, blank=True)
    gestational_age_weeks = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_weight_g = models.PositiveIntegerField(null=True, blank=True)
    apgar_1min = models.PositiveSmallIntegerField(null=True, blank=True)
    apgar_5min = models.PositiveSmallIntegerField(null=True, blank=True)
    neonatal_complications = models.TextField(blank=True)
    other = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "birth_history_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_birth_history_version"
            )
        ]
        

class PediatricNutritionHistory(ClinicalFindingBase):
    """Feeding / nutrition history for infants and children."""

    feeding_type = models.CharField(max_length=64, blank=True)  # exclusive breast, mixed, formula...
    breastfeeding_duration_months = models.PositiveSmallIntegerField(null=True, blank=True)
    exclusive_breastfeeding = models.BooleanField(null=True, blank=True)
    formula_used = models.CharField(max_length=128, blank=True)
    complementary_feeding_start_months = models.PositiveSmallIntegerField(null=True, blank=True)
    current_diet = models.TextField(blank=True)
    appetite = models.CharField(max_length=64, blank=True)
    feeding_difficulties = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "pediatric_nutrition_history"


class PediatricNutritionHistoryHistory(UUIDPrimaryKeyModel):
    finding = models.ForeignKey(
        PediatricNutritionHistory, on_delete=models.CASCADE, related_name="history_rows"
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
    feeding_type = models.CharField(max_length=64, blank=True)
    breastfeeding_duration_months = models.PositiveSmallIntegerField(null=True, blank=True)
    complementary_feeding_start_months = models.PositiveSmallIntegerField(null=True, blank=True)
    current_diet = models.TextField(blank=True)
    feeding_difficulties = models.TextField(blank=True)
    other = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "pediatric_nutrition_history_history"
        constraints = [
            models.UniqueConstraint(
                fields=["finding", "version"],
                name="unique_pediatric_nutrition_history_version"
            )
        ]
        
        

