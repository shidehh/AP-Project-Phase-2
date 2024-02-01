from django.shortcuts import render
from django.http import JsonResponse
from Patient.models import PatientAppointment
from Clinic.models import Clinic


SECRETARY_SPECIAL_CODE = 's1234567@c'


def enter_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == SECRETARY_SPECIAL_CODE:
            return JsonResponse({"success": True},status = 200)
        else:
            return JsonResponse({"success": False, "message": "The secretary special code is wrong."}, status = 400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status = 405)


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
        return JsonResponse(patient_info, safe=False, status = 200)
    else:
        return JsonResponse({"message": "Invalid request method."}, status = 405)


# the view code with render function : 
'''from django.shortcuts import render
from Patient.models import PatientAppointment
from Clinic.models import Clinic

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
        patients = [a.patient for a in appointments]
        patient_info = [{
            "patient_national_code": p.patient_national_code,
            "patient_name": p.patient_name,
            "patient_age": p.patienthealth.patient_age,
            "patient_insurance": p.patienthealth.patient_insurance,
            "patient_contact_info": p.patient_contact_info,
            "patient_reserved_appointments": p.patientappointment.reserved
        } for p in patients]
        return render(request, 'secretary_after_login.html', {"patient_info": patient_info})
    else:
        return render(request, 'secretary_page.html', {"message": "Invalid request method."})'''

