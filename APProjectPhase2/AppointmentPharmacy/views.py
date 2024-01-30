from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import Appointment, Pharmacy
from Patient.models import PatientInfo
from Clinic.models import Clinic
# Create your views here.
  

def reserve_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        reserved = request.POST.get('reserved')
        appointment = Appointment.objects.get(id=appointment_id)

        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': appointment.clinic.id, 'reserved': reserved}
        response = requests.post(url, json=data)
        result = response.json()

        if result['success']:
            appointment.reserved += int(reserved)
            appointment.save()

        return JsonResponse(result)
    else:
        return JsonResponse({"message": "Invalid request method."})

def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        cancelled = request.POST.get('cancelled')
        appointment = Appointment.objects.get(id=appointment_id)

        appointment.reserved -= int(cancelled)
        appointment.save()

        return JsonResponse({"success": True, "message": "Appointment cancelled successfully"})
    else:
        return JsonResponse({"message": "Invalid request method."})

def increase_capacity(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        increase_amount = request.POST.get('increase_amount')
        clinic = Clinic.objects.get(id=clinic_id)

        clinic.capacity += int(increase_amount)
        clinic.save()

        return JsonResponse({"success": True, "message": "Clinic capacity increased successfully"})
    else:
        return JsonResponse({"message": "Invalid request method."})


def check_patient(request, patient_national_code):
    if request.method == 'GET':
        exists = PatientInfo.objects.filter(patient_national_code=patient_national_code).exists()
        return JsonResponse({"exists": exists})
    else:
        return JsonResponse({"message": "Invalid request method."})

def check_insurance(request, patient_national_code):
    if request.method == 'GET':
        patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        has_insurance = patient.patient_insurance == 'Yes'
        return JsonResponse({"has_insurance": has_insurance})
    else:
        return JsonResponse({"message": "Invalid request method."})

def dispense_drug(request, drug, patient_national_code):
    if request.method == 'POST':
        pharmacy = Pharmacy.objects.get(drug_name=drug)
        if pharmacy.quantity > 0:
            pharmacy.quantity -= 1
            pharmacy.save()
            return JsonResponse({"success": True, "message": "We have your drug in stock.\nThanks for your shopping!"})
        else:
            return JsonResponse({"success": False, "message": f"Sorry, {drug} is currently out of stock."})
    else:
        return JsonResponse({"message": "Invalid request method."})

def check_availability(request, drug):
    if request.method == 'GET':
        available = Pharmacy.objects.filter(drug_name=drug, quantity__gt=0).exists()
        return JsonResponse({"available": available})
    else:
        return JsonResponse({"message": "Invalid request method."})
