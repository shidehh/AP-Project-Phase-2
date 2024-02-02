from django.shortcuts import render,redirect
from Clinic.models import Clinic
from .models import PatientInfo, PatientAppointment
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
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
        if password_type == 'permanent':
            password = request.POST.get('password')
        else:
            password = generate_password(10)  # Generate a temporary password
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
        try:
            user = PatientInfo.objects.get(username=national_code)
        except PatientInfo.DoesNotExist:
            return render(request, 'patient_page.html', {"message": "Patient does not exist. Please sign up."})
        
        # Check if the user chose a temporary password
        if user.password_type == 'temporary':
            temp_password = generate_password(10)  # Generate the temporary password once
            hashed_temp_password = make_password(temp_password)
            if check_password(password, hashed_temp_password):
                login(request, user)
                return render(request, 'patient_temporary.html', {"message": "Log in successfully!"})
            else:
                return render(request, 'patient_page.html', {"message": "Invalid temporary password."})
        else:
            # Check the permanent password
            if user.check_password(password):
                login(request, user)
                return render(request, 'patient_permanent.html', {"message": "Log in successfully!"})
            else:
                return render(request, 'patient_page.html', {"message": "Invalid password."})
    else:
        return render(request, 'patient_page.html', {"message": "Invalid request method."})

'''def logout_view(request):
    logout(request)
    return redirect('main.html')'''

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
        try:
            patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        except PatientInfo.DoesNotExist:
            return render(request, 'patient_page.html', {"message": "Patient does not exist."})

        appointments = PatientAppointment.objects.filter(patient=patient)
        return render(request, 'patient_after_login.html', {
            "patient_national_code": patient.patient_national_code,
            "patient_name": patient.patient_name,
            "appointments": [{"clinic_id": a.clinic.id, "reserved": a.reserved} for a in appointments]
        })
    else:
        return render(request, 'patient_page.html', {"message": "Invalid request method."})