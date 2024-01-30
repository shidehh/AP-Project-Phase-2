from django.shortcuts import render
from django.http import JsonResponse
from Patient.models import PatientAppointment
from Clinic.models import Clinic

# Create your views here.

SECRETARY_SPECIAL_CODE = 's1234567@c'


def enter_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == SECRETARY_SPECIAL_CODE:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "The secretary special code is wrong."})
    else:
        return JsonResponse({"message": "Invalid request method."})


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
        return JsonResponse(patient_info, safe=False)
    else:
        return JsonResponse({"message": "Invalid request method."})
