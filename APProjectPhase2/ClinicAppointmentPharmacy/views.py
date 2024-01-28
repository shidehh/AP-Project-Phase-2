from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import Clinic, Appointment, Pharmacy
from Patient.models import PatientInfo
# Create your views here.

def update_from_api(request):
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:5000/slots')
        data = response.json()

        additional_info = {
            "1": {"service": "ophthalmology", "address": "Los Angeles; Beverly Hills", "contact": "09123758274"},
            "2": {"service": "gynecology", "address": "900 Pacific Ave, Everett", "contact": "09194726482"},
            "3": {"service": "otolaryngology", "address": "Harborview, 325 9th Ave, Seattle", "contact": "09185746253"},
            "4": {"service": "general", "address": "Hoyt Ave, Everett", "contact": "09109584726"},
            "5": {"service": "orthopedics", "address": "45th St, Seattle", "contact": "09108876543"},
            "6": {"service": "cardiology", "address": "Cleveland, Ohio", "contact": "09124837264"},
            "7": {"service": "dental", "address": "Alderwood Mall Blvd, Lynnwood", "contact": "09127564728"},
        }

        if data is not None:
            for clinic_id, capacity in data.items():
                info = additional_info.get(clinic_id, {})
                service = info.get("service", "")
                address = info.get("address", "")
                contact = info.get("contact", "")
                # in order to debuf or check, we can use clinic and created. not necessary
                clinic, created = Clinic.objects.update_or_create(
                    id=clinic_id,
                    defaults={
                        'capacity': capacity,
                        'service': service,
                        'address': address,
                        'clinic_contact_info': contact
                    }
                )

        return JsonResponse({"message": "Clinic capacities updated successfully."})
    else:
        return JsonResponse({"message": "Invalid request method."})

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
