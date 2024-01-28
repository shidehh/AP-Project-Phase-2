from django.shortcuts import render
from ClinicAppointmentPharmacy.models import Clinic
from .models import PatientInfo, PatientAppointment
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        national_code = request.POST.get('national_code')
        name = request.POST.get('name')
        contact_info = request.POST.get('contact_info')
        password = request.POST.get('password')
        patient = PatientInfo.objects.create_user(username=national_code, password=password)
        patient.patient_name = name
        patient.patient_contact_info = contact_info
        patient.save()
        return JsonResponse({"message": "Sign up successfully. Now you need to log in to be able to reserve or cancel an appointment."})
    else:
        return JsonResponse({"message": "Invalid request method."})

def log_in(request):
    if request.method == 'POST':
        national_code = request.POST.get('national_code')
        password = request.POST.get('password')
        user = authenticate(request, username=national_code, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Log in successfully!"})
        else:
            return JsonResponse({"message": "Invalid national code or password."})
    else:
        return JsonResponse({"message": "Invalid request method."})

def log_out(request):
    logout(request)
    return JsonResponse({"message": "You have been logged out."})

def select_clinic_capacity_info(request, clinic_id):
    if request.method == 'GET':
        clinic = Clinic.objects.get(id=clinic_id)
        return JsonResponse({
            "clinic_id": clinic.id,
            "service": clinic.service,
            "capacity": clinic.capacity,
            "clinic_reserved_appointments": clinic.clinic_reserved_appointments,
            "address": clinic.address,
            "clinic_contact_info": clinic.clinic_contact_info
        })
    else:
        return JsonResponse({"message": "Invalid request method."})

def select_patient_reserved_appointments_info(request, patient_national_code):
    if request.method == 'GET':
        patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        appointments = PatientAppointment.objects.filter(patient=patient)
        return JsonResponse({
            "patient_national_code": patient.patient_national_code,
            "patient_name": patient.patient_name,
            "appointments": [{"clinic_id": a.clinic.id, "reserved": a.reserved} for a in appointments]
        })
    else:
        return JsonResponse({"message": "Invalid request method."})
