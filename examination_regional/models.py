from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from examination.models import ClinicalFindingBase

# Create your models here.
class HeadAndNeckExam(ClinicalFindingBase):
    """Head and neck examination (especially useful in trauma)."""

    scalp_skull = models.TextField(blank=True)
    face = models.TextField(blank=True)
    eyes = models.TextField(blank=True)
    ears = models.TextField(blank=True)
    nose = models.TextField(blank=True)
    mouth_teeth = models.TextField(blank=True)
    neck = models.TextField(blank=True)
    cervical_spine = models.TextField(blank=True)
    lymph_nodes = models.TextField(blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "head_and_neck_exam"
        
        

class UpperLimbExam(ClinicalFindingBase):
    """Upper limbs examination."""

    side = models.CharField(max_length=16, blank=True)  # left, right, both
    inspection = models.TextField(blank=True)
    palpation = models.TextField(blank=True)
    range_of_motion = models.TextField(blank=True)
    strength = models.TextField(blank=True)
    neurovascular = models.TextField(blank=True)
    joints = models.TextField(blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "upper_limb_exam"
        


class LowerLimbExam(ClinicalFindingBase):
    """Lower limbs examination."""

    side = models.CharField(max_length=16, blank=True)
    inspection = models.TextField(blank=True)
    palpation = models.TextField(blank=True)
    range_of_motion = models.TextField(blank=True)
    strength = models.TextField(blank=True)
    neurovascular = models.TextField(blank=True)
    joints = models.TextField(blank=True)
    gait = models.CharField(max_length=128, blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "lower_limb_exam"
        


class ThoracicAbdominalExam(ClinicalFindingBase):
    """Thoracic and abdominal wall / regional examination (trauma or local findings)."""

    thorax_inspection = models.TextField(blank=True)
    thorax_palpation = models.TextField(blank=True)
    abdomen_inspection = models.TextField(blank=True)
    abdomen_palpation = models.TextField(blank=True)
    abdomen_percussion = models.TextField(blank=True)
    abdomen_auscultation = models.TextField(blank=True)
    pelvic = models.TextField(blank=True)

    findings = models.TextField(blank=True)
    other = models.TextField(blank=True)

    class Meta:
        db_table = "thoracic_abdominal_exam"
        


