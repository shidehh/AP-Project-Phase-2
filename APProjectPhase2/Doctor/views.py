from django.shortcuts import render
from Patient.models import PatientInfo, PatientHealth, PatientAppointment
from Clinic.models import Clinic
from django.contrib.auth import logout

# Create your views here.

DOCTOR_SPECIAL_CODE = 'd7654321_doc*'

def enter_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == DOCTOR_SPECIAL_CODE:
            return render(request, 'doctor_after_login.html')
        else:
            return render(request, 'doctor_page.html', {"message": "The doctor special code is wrong."})
    else:
        return render(request, 'doctor_page.html', {"message": "Invalid request method."})

def select_each_clinic_info(request, clinic_id):
    if request.method == 'GET':
        clinic = Clinic.objects.get(id=clinic_id)
        appointments = PatientAppointment.objects.filter(clinic=clinic, reserved__gt=0)
        patients = [a.patient for a in appointments]
        patient_info = [{
            "patient_national_code": p.patient_national_code,
            "patient_name": p.patient_name,
            "patient_age": p.patienthealth.patient_age,
            "patient_insurance": p.patienthealth.patient_insurance,
            "patient_contact_info": p.patient_contact_info,
            "patient_reserved_appointments": p.patientappointment.reserved
        } for p in patients]
        return render(request, 'doctor_patient_see.html', {"patient_info": patient_info})
    else:
        return render(request, 'doctor_page.html', {"message": "Invalid request method."})

def select_each_patient_info(request, patient_national_code):
    if request.method == 'GET':
        try:
            patient = PatientInfo.objects.get(patient_national_code=patient_national_code)
        except PatientInfo.DoesNotExist:
            return render(request, 'doctor_page.html', {"message": "Patient does not exist."})
        patient_health = PatientHealth.objects.get(patient=patient)
        patient_appointments = PatientAppointment.objects.filter(patient=patient)
        patient_info = {
                "patient_national_code": patient.patient_national_code,
                "patient_name": patient.patient_name,
                "patient_age": patient_health.patient_age,
                "patient_insurance": patient_health.patient_insurance,
                "patient_contact_info": patient.patient_contact_info,
                "patient_reserved_appointments": [a.reserved for a in patient_appointments]
            }
        return render(request, 'doctor_patient_info_view.html', {"patient_info": patient_info})
    else:
        return render(request, 'doctor_page.html', {"message": "Invalid request method."})
    
'''def logout_view(request):
    logout(request)
    return redirect('main_page.html')'''
