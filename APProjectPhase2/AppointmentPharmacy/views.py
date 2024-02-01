from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import Appointment, Pharmacy
from Patient.models import PatientInfo
from Clinic.models import Clinic
# Create your views here.
  
def reserve_appointment(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        number_of_reservations = request.POST.get('number_of_reservations')
        patient_national_code = request.POST.get('patient_national_code')

        # Get the clinic and patient based on the provided IDs
        clinic = Clinic.objects.get(id=clinic_id)
        patient = PatientInfo.objects.get(national_code=patient_national_code)

        # Create a new appointment or get an existing one
        appointment, created = Appointment.objects.get_or_create(clinic=clinic, patient=patient)
        
        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': clinic.id, 'reserved': number_of_reservations}
        response = requests.post(url, json=data)
        result = response.json()

        if result['success']:
            appointment.reserved += int(number_of_reservations)
            appointment.save()

        return JsonResponse(result)
    else:
        return JsonResponse({"message": "Invalid request method."})

def cancel_appointment(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        number_of_cancellations = request.POST.get('number_of_cancellations')
        patient_national_code = request.POST.get('patient_national_code')

        # Get the clinic and patient based on the provided IDs
        clinic = Clinic.objects.get(id=clinic_id)
        patient = PatientInfo.objects.get(national_code=patient_national_code)

        # Get the appointment for the clinic and patient
        appointment = Appointment.objects.get(clinic=clinic, patient=patient)

        appointment.reserved -= int(number_of_cancellations)
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


def pharmacy_view(request):
    if request.method == 'POST':
        # Get the drug name from the form data
        drug = request.POST.get('drug')

        # Get the patient from the session
        patient = PatientInfo.objects.get(national_code=request.session['patient_national_code'])

        # Get the pharmacy
        pharmacy = Pharmacy.objects.get(id=1)  # Assuming there's only one Pharmacy

        # Check if the drug is in stock
        if pharmacy.check_availability(drug):
            # Dispense the drug and update the inventory
            pharmacy.dispense_drug(drug, patient)

            # Check the patient's insurance status and add the appropriate message
            if patient.check_insurance():
                message = 'You have 70 percent discount as you have insurance.'
            else:
                message = 'You have to pay full price as you do not have insurance.'

            # Add the success message
            message += ' We have your drug in stock. Thanks for your shopping!'

            # Return a JsonResponse with the message
            return JsonResponse({'message': message})
        else:
            # Return a JsonResponse with the error message
            return JsonResponse({'message': f'Sorry, {drug} is currently out of stock.'})
    else:
        # Render the pharmacy page
        return render(request, 'pharmacy.html')
