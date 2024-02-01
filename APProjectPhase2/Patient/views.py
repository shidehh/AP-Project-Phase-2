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
'''from django.shortcuts import render
from Clinic.models import Clinic
from .models import PatientInfo, PatientAppointment
from django.contrib.auth import authenticate, login, logout
import string
import random

def generate_password(length):
    characters = string.ascii_lowercase + string.digits 
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def sign_up(request):
    if request.method == 'POST':
        national_code = request.POST.get('national_code')
        name = request.POST.get('name')
        contact_info = request.POST.get('contact_info')
        password_type = int(request.POST.get('password_type'))
        password = None
        if password_type == 2:
            password = request.POST.get('password')
        patient = PatientInfo.objects.create_user(username=national_code, password=password)
        patient.patient_name = name
        patient.patient_contact_info = contact_info
        patient.save()
        return render(request, 'patient_page.html', {"message": "Sign up successfully. Now you need to log in to be able to reserve or cancel an appointment."})
    else:
        return render(request, 'patient_sign_up.html', {"message": "Invalid request method."})

def log_in(request):
    if request.method == 'POST':
        national_code = request.POST.get('national_code')
        password = request.POST.get('password')
        user = authenticate(request, username=national_code, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'patient_after_login.html', {"message": "Log in successfully!"})
        else:
            temp_password = generate_password(10)  # Generate a temporary password
            print(f"Your temporary password is: {temp_password}")
            entered_temp_password = input("Please enter the temporary password: ")
            if entered_temp_password == temp_password:
                login(request, user)
                return render(request, 'patient_after_login.html', {"message": "Log in successfully!"})
            else:
                return render(request, 'patient_page.html', {"message": "Invalid temporary password."})
    else:
        return render(request, 'patient_page.html', {"message": "Invalid request method."})

def log_out(request):
    logout(request)
    return render(request, 'patient_page.html', {"message": "You have been logged out."})

def select_clinic_capacity_info(request, clinic_id):
    if request.method == 'GET':
        clinic = Clinic.objects.get(id=clinic_id)
        return render(request, 'patient_after_login.html', {
            "clinic_id": clinic.id,
            "service": clinic.service,
            "capacity": clinic.capacity,
            "clinic_reserved_appointments": clinic.clinic_reserved_appointments,
            "address": clinic.address,
            "clinic_contact_info": clinic.clinic_contact_info
        })
    else:
        return render(request, 'patient_page.html', {"message": "Invalid request method."})

def select_patient_reserved_appointments_info(request, patient_national_code):
    if request.method == 'GET':
        patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        appointments = PatientAppointment.objects.filter(patient=patient)
        return render(request, 'patient_after_login.html', {
            "patient_national_code": patient.patient_national_code,
            "patient_name": patient.patient_name,
            "appointments": [{"clinic_id": a.clinic.id, "reserved": a.reserved} for a in appointments]
        })
    else:
        return render(request, 'patient_page.html', {"message": "Invalid request method."})'''