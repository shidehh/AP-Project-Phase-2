# Create your models here.
import requests
from django.db import models
# patients app, PtientInfo corresponds to patient_info table
from patients.models import PatientInfo

class Clinic(models.Model):
    # Define your fields here
    capacity = models.IntegerField()
    service = models.CharField(max_length=255)
    clinic_reserved_appointments = models.IntegerField()
    address = models.CharField(max_length=255)
    clinic_contact_info = models.CharField(max_length=255)

    @classmethod
    def update_from_api(cls):
        # Send GET request to Flask API
        response = requests.get('http://127.0.0.1:5000/slots')
        data = response.json()

        # Update database
        if data is not None:
            for clinic_id, capacity in data.items():
                # Fetch the clinic from the database, or create a new one if it doesn't exist
                clinic, created = cls.objects.get_or_create(id=clinic_id)

                # Update the clinic's capacity
                clinic.capacity = capacity
                clinic.save()


class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, to_field='patient_national_code')
    reserved = models.IntegerField(default=0)

    def reserve_appointment(self, reserved):
        # Send POST request to Flask API
        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': self.clinic.id, 'reserved': reserved}
        response = requests.post(url, json=data)
        result = response.json()

        if result['success']:
            # Update Django database
            self.reserved += reserved
            self.save()

        return result

    def cancel_appointment(self, cancelled):
        # Update Django database
        self.reserved -= cancelled
        self.save()

        return {"success": True, "message": "Appointment cancelled successfully"}

    def increase_capacity(self, increase_amount):
        # Update Django database
        self.clinic.capacity += increase_amount
        self.clinic.save()

        return {"success": True, "message": "Clinic capacity increased successfully"}


class Pharmacy(models.Model):
    drug_name = models.CharField(max_length=255, primary_key=True)
    quantity = models.IntegerField()

    def check_patient(self, patient_national_code):
        # Check if the patient exists
        return PatientInfo.objects.filter(patient_national_code=patient_national_code).exists()

    def check_insurance(self, patient_national_code):
        # Check if the patient has insurance
        patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        return patient.patient_insurance == 'Yes'

    def dispense_drug(self, drug, patient_national_code):
        # Check if the patient exists
        if not self.check_patient(patient_national_code):
            return False

        # Check if the drug is in stock
        if not self.check_availability(drug):
            print(f'Sorry, {drug} is currently out of stock.\n')
            return False

        # Dispense the drug and update the inventory
        self.update_inventory(drug)

        # Check the patient's insurance status and print the appropriate message
        if self.check_insurance(patient_national_code):
            print('You have 70 percent discount as you have insurance.')
        else:
            print('You have to pay full price as you do not have insurance.')

        print('We have your drug in stock.\nThanks for your shopping!')
        return True

    def check_availability(self, drug):
        # Check if the drug is in stock
        return Pharmacy.objects.filter(drug_name=drug, quantity__gt=0).exists()

    def update_inventory(self, drug):
        try:
            # Dispense the drug and update the inventory
            pharmacy = Pharmacy.objects.get(drug_name=drug)
            pharmacy.quantity -= 1
            pharmacy.save()
        except Exception as e:
            print(f'An error occurred: {e}')
