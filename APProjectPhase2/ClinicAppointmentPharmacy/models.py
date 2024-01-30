from django.db import models
from Patient.models import PatientInfo
from Clinic.models import Clinic


# Create your models here.

class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, to_field='patient_national_code')
    reserved = models.IntegerField(default=0)

class Pharmacy(models.Model):
    drug_name = models.CharField(max_length=255, primary_key=True)
    quantity = models.IntegerField()
