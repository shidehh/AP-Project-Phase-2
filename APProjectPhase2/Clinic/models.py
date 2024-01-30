from django.db import models

# Create your models here.
class Clinic(models.Model):
    id = models.IntegerField(primary_key=True)
    capacity = models.IntegerField()
    service = models.CharField(max_length=255)
    clinic_reserved_appointments = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    clinic_contact_info = models.CharField(max_length=255)