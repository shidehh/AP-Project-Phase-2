from django.db import models


class Clinic(models.Model):
    clinic_id = models.IntegerField(primary_key=True)
    capacity = models.IntegerField()
    service = models.CharField(max_length=100)
    clinic_reserved_appointments = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    clinic_contact_info = models.CharField(max_length=20)
