
from django.shortcuts import render,redirect
from Patient.models import PatientAppointment
from Clinic.models import Clinic
from django.contrib.auth import logout

SECRETARY_SPECIAL_CODE = 's1234567@c'

def enter_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == SECRETARY_SPECIAL_CODE:
            return render(request, 'secretary_after_login.html')
        else:
            return render(request, 'secretary_page.html', {"message": "The secretary special code is wrong."})
    else:
        return render(request, 'secretary_page.html', {"message": "Invalid request method."})

def select_each_clinic_info(request, clinic_id):
    if request.method == 'GET':
        clinic = Clinic.objects.get(id=clinic_id)
        appointments = PatientAppointment.objects.filter(clinic=clinic, reserved__gt=0)
        patient_info = []
        for a in appointments:
            try:
                patient = a.patient
            except AttributeError:
                continue  # Skip this appointment if there's no patient

            patient_info.append({
                "patient_national_code": patient.patient_national_code,
                "patient_name": patient.patient_name,
                "patient_age": patient.patienthealth.patient_age,
                "patient_insurance": patient.patienthealth.patient_insurance,
                "patient_contact_info": patient.patient_contact_info,
                "patient_reserved_appointments": patient.patientappointment.reserved
            })

        return render(request, 'secretary_after_login.html', {"patient_info": patient_info})
    else:
        return render(request, 'secretary_page.html', {"message": "Invalid request method."})

def logout_view(request):
    logout(request)
    return redirect('main.html')
