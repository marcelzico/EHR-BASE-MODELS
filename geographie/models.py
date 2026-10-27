from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

class Province(UUIDPrimaryKeyModel, TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=32, blank=True)  # official code if any
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "geo_province"
        ordering = ["name"]


class Region(UUIDPrimaryKeyModel, TimeStampedModel):
    province = models.ForeignKey(
        Province, on_delete=models.PROTECT, related_name="regions"
    )
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "geo_region"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["province", "name"],
                name="unique_region_per_province"
            )
        ]


class District(UUIDPrimaryKeyModel, TimeStampedModel):
    region = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="districts"
    )
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "geo_district"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["region", "name"],
                name="unique_district_per_region"
            )
        ]


class Commune(UUIDPrimaryKeyModel, TimeStampedModel):
    district = models.ForeignKey(
        District, on_delete=models.PROTECT, related_name="communes"
    )
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "geo_commune"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["district", "name"],
                name="unique_commune_per_district"
            )
        ]


class Fokontany(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Lowest level. Not always known (there are > 10 000 in the country).
    Stored when available.
    """
    commune = models.ForeignKey(
        Commune, on_delete=models.PROTECT, related_name="fokontany_list"
    )
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "geo_fokontany"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["commune", "name"],
                name="unique_fokontany_per_commune"
            )
        ]
        
    