from django.db import models
from shared_models.models import UUIDPrimaryKeyModel, TimeStampedModel
from organization_location.models import Organization

class User(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Login identity. Links to Django auth or a custom auth system later.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Link to the person profile
    person = models.OneToOneField(
        "Person", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="user_account"
    )

    class Meta:
        db_table = "user_account"


class Person(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Shared demographic profile for any human in the system
    (staff, student, intern…).
    """
    family_name = models.CharField(max_length=128)
    given_name = models.CharField(max_length=128, blank=True)
    gender = models.CharField(max_length=16, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "person"
        
        
class Practitioner(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Clinical professional who can be author, performer, requester...
    """
    person = models.OneToOneField(
        Person, on_delete=models.PROTECT, related_name="practitioner_profile"
    )
    active = models.BooleanField(default=True)

    # Professional identifiers
    license_number = models.CharField(max_length=64, blank=True)
    specialty = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "practitioner"
        

class StaffRole(models.TextChoices):
    PRACTITIONER = "practitioner", "Practitioner"
    NURSE = "nurse", "Nurse"
    PHARMACIST = "pharmacist", "Pharmacist"
    RECEPTIONIST = "receptionist", "Receptionist"
    CASHIER = "cashier", "Cashier"
    SECRETARY = "secretary", "Secretary"
    ADMINISTRATOR = "administrator", "Administrator"
    OTHER = "other", "Other"


class StaffAssignment(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Assigns a Person to a Service/Department with a specific role.
    """
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="staff_assignments"
    )
    organization = models.ForeignKey(          # Service / Department
        Organization, on_delete=models.PROTECT, related_name="staff_assignments"
    )
    role = models.CharField(max_length=32, choices=StaffRole.choices)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "staff_assignment"
        indexes = [
            models.Index(fields=["person", "active"]),
            models.Index(fields=["organization", "role"]),
        ]
        
        
class Student(UUIDPrimaryKeyModel, TimeStampedModel):
    """Medical or paramedical student."""
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="student_profile"
    )
    student_number = models.CharField(max_length=64, blank=True)
    school = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "student"


class Intern(UUIDPrimaryKeyModel, TimeStampedModel):
    """Intern / resident in training."""
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="intern_profile"
    )
    intern_number = models.CharField(max_length=64, blank=True)
    specialty = models.CharField(max_length=128, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    # Current placement
    current_service = models.ForeignKey(
        Organization, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="current_interns"
    )

    class Meta:
        db_table = "intern"
        


