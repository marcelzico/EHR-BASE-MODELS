from django.db import models

# Create your models here.
class Result(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Overall result / report for an Order (laboratory, imaging, other).
    """
    STATUS_CHOICES = [
        ("preliminary", "Preliminary"),
        ("final", "Final"),
        ("amended", "Amended"),
        ("corrected", "Corrected"),
        ("cancelled", "Cancelled"),
        ("entered-in-error", "Entered in Error"),
    ]

    CATEGORY_CHOICES = [
        ("laboratory", "Laboratory"),
        ("imaging", "Imaging"),
        ("other", "Other"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="results"
    )
    encounter = models.ForeignKey(
        Encounter, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="results"
    )
    order = models.ForeignKey(
        Order, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="results"
    )

    category = models.CharField(
        max_length=32, choices=CATEGORY_CHOICES, default="laboratory"
    )
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="final"
    )

    # What this result is about
    code_system = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=64, blank=True)
    code_display = models.CharField(max_length=255, blank=True)
    code_text = models.CharField(max_length=255, blank=True)  # e.g. "Complete Blood Count"

    # Overall conclusion (very important for imaging & some lab reports)
    conclusion = models.TextField(blank=True)

    issued_at = models.DateTimeField(null=True, blank=True)
    effective_at = models.DateTimeField(null=True, blank=True)  # period the result refers to

    performer = models.ForeignKey(
        Practitioner, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="performed_results"
    )
    # Can later also point to Organization (lab, radiology dept)

    # Optional link to a previous result when amending/correcting
    replaces = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="replaced_by"
    )

    note = models.TextField(blank=True)

    class Meta:
        db_table = "result"
        indexes = [
            models.Index(fields=["patient", "issued_at"]),
            models.Index(fields=["encounter"]),
            models.Index(fields=["order"]),
            models.Index(fields=["category", "status"]),
        ]
        


class ResultItem(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    One line / analyte / discrete finding inside a Result.
    Used for lab panels and structured imaging findings.
    """
    result = models.ForeignKey(
        Result, on_delete=models.CASCADE, related_name="items"
    )

    code_system = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=64, blank=True)
    code_display = models.CharField(max_length=255, blank=True)
    code_text = models.CharField(max_length=255, blank=True)

    # Value
    value_quantity = models.DecimalField(
        max_digits=16, decimal_places=4, null=True, blank=True
    )
    value_unit = models.CharField(max_length=64, blank=True)
    value_string = models.TextField(blank=True)
    value_code = models.CharField(max_length=64, blank=True)
    value_code_display = models.CharField(max_length=255, blank=True)

    interpretation = models.CharField(max_length=64, blank=True)  # normal, high, low, critical...
    reference_range = models.CharField(max_length=128, blank=True)

    note = models.TextField(blank=True)

    class Meta:
        db_table = "result_item"
        indexes = [
            models.Index(fields=["result"]),
            models.Index(fields=["code_system", "code"]),
        ]
        
        
class ResultHistory(UUIDPrimaryKeyModel):
    result = models.ForeignKey(
        Result, on_delete=models.CASCADE, related_name="history_rows"
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
    conclusion = models.TextField(blank=True)
    code_text = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "result_history"
        constraints = [
            models.UniqueConstraint(
                fields=["result", "version"],
                name="unique_result_version"
            )
        ]
        
