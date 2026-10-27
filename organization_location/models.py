from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel


class Organization(UUIDPrimaryKeyModel, TimeStampedModel):
    """Hospital, department, external lab, etc."""
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64, blank=True)  # hospital, dept, lab...
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="children"
    )
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "organization"


class Location(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Physical or logical place.
    Hierarchy: Facility → Building → Ward → Room → Bed
    """
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=64, blank=True)
    physical_type = models.CharField(max_length=64)  # facility, ward, room, bed, theatre...
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="children"
    )
    organization = models.ForeignKey(
        Organization, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="locations"
    )
    status = models.CharField(max_length=32, default="active")  # active, inactive, suspended...
    operational_status = models.CharField(max_length=32, blank=True)  # occupied, closed, housekeeping...

    class Meta:
        db_table = "location"