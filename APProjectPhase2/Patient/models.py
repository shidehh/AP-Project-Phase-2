from django.db import models
from Clinic.models import Clinic


class PatientInfo(models.Model):
    patient_national_code = models.CharField(max_length=10, primary_key=True)
    patient_name = models.CharField(max_length=255)
    patient_contact_info = models.CharField(max_length=255)
    patient_password = models.CharField(max_length=255)


class PatientHealth(models.Model):
    INSURANCE_CHOICES = [
        ('yes', 'yes'),
        ('no', 'no'),
    ]

    patient = models.OneToOneField(PatientInfo, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField()
    insurance = models.CharField(max_length=3, choices=INSURANCE_CHOICES)



class PatientAppointment(models.Model):
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)
    patient_reserved_appointments = models.IntegerField(default=0)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
