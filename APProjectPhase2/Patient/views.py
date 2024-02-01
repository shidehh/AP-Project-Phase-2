from django.shortcuts import render
from Clinic.models import Clinic
from .models import PatientInfo, PatientAppointment
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


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
        return JsonResponse({"message": "Sign up successfully. Now you need to log in to be able to reserve or cancel an appointment."}, status = 201)
    else:
        return JsonResponse({"message": "Invalid request method."}, status = 405)

def log_in(request):
    if request.method == 'POST':
        national_code = request.POST.get('national_code')
        password = request.POST.get('password')
        user = authenticate(request, username=national_code, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Log in successfully!"}, status = 200)
        else:
            return JsonResponse({"message": "Invalid national code or password."}, status = 401)
    else:
        return JsonResponse({"message": "Invalid request method."}, status = 405)

def log_out(request):
    logout(request)
    return JsonResponse({"message": "You have been logged out."}, status = 200)

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
        return JsonResponse({"message": "Invalid request method."}, status = 405)

def select_patient_reserved_appointments_info(request, patient_national_code):
    if request.method == 'GET':
        patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        appointments = PatientAppointment.objects.filter(patient=patient)
        return JsonResponse({
            "patient_national_code": patient.patient_national_code,
            "patient_name": patient.patient_name,
            "appointments": [{"clinic_id": a.clinic.id, "reserved": a.reserved} for a in appointments]
        }, status = 200)
    else:
        return JsonResponse({"message": "Invalid request method."}, status = 405)


# the view code with render function : 
