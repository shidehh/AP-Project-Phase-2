from django.db import models
from Patient.models import PatientInfo

'''from django.apps import apps

PatientInfo = apps.get_model('Patient', 'PatientInfo')'''

# Create your models here.

class Clinic(models.Model):
    id = models.IntegerField(primary_key=True)
    capacity = models.IntegerField()
    service = models.CharField(max_length=255)
    clinic_reserved_appointments = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    clinic_contact_info = models.CharField(max_length=255)


class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, to_field='patient_national_code')
    reserved = models.IntegerField(default=0)

class Pharmacy(models.Model):
    drug_name = models.CharField(max_length=255, primary_key=True)
    quantity = models.IntegerField()
