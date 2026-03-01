import secrets
from django.db import models
from django.contrib.auth.models import AbstractUser

def generate_staff_id():
    return "S" + secrets.token_hex(6).upper()

ROLE = (
    ("ADMIN", "Admin"),
    ("ANALYST", "Analyst"),
)

class Staff(AbstractUser):
    staff_id = models.CharField(max_length=25, unique=True, default=generate_staff_id)
    role = models.CharField(max_length=20, choices=ROLE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "staff"
        ordering = ["-created_at"]
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
