
from django.shortcuts import render,redirect
from .models import Appointment, Pharmacy
from Clinic.models import Clinic
from Patient.models import PatientInfo, PatientHealth
import requests
from django.contrib.auth import logout

def reserve_appointment(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        number_of_reservations = request.POST.get('number_of_reservations')
        patient_national_code = request.POST.get('patient_national_code')
        user_type = request.POST.get('user_type')

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
            if user_type == 'patient':
                return render(request, 'patient_available_appointment.html', {"message": "Appointment reserved successfully"})
            else:
                return render(request, 'secretary_reserve_appointment.html', {"message": "Appointment reserved successfully"})
        else:
            if user_type == 'patient':
                return render(request, 'patient_available_appointment.html', {"message": "Failed to reserve appointment"})
            else:
                return render(request, 'secretary_reserve_appointment.html', {"message": "Failed to reserve appointment"})
    else:
        return render(request, 'patient_available_appointment.html', {"message": "Invalid request method."})

def cancel_appointment(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        number_of_cancellations = request.POST.get('number_of_cancellations')
        patient_national_code = request.POST.get('patient_national_code')
        user_type = request.POST.get('user_type')

        # Get the clinic and patient based on the provided IDs
        clinic = Clinic.objects.get(id=clinic_id)
        patient = PatientInfo.objects.get(national_code=patient_national_code)

        # Get the appointment for the clinic and patient
        appointment = Appointment.objects.get(clinic=clinic, patient=patient)

        appointment.reserved -= int(number_of_cancellations)
        appointment.save()

        if user_type == 'patient':
            return render(request, 'patient_reserved_appointment.html', {"message": "Appointment cancelled successfully"})
        else:
            return render(request, 'secretary_cancel_appointment.html', {"message": "Appointment cancelled successfully"})
    else:
        return render(request, 'patient_reserved_appointment.html', {"message": "Invalid request method."})

def increase_capacity(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        increase_amount = request.POST.get('increase_amount')
        clinic = Clinic.objects.get(id=clinic_id)
        clinic.capacity += int(increase_amount)
        clinic.save()
        return render(request, 'secretary_increase_capacity.html', {"message": "Clinic capacity increased successfully"})
    else:
        return render(request, 'secretary_increase_capacity.html', {"message": "Invalid request method."})

def pharmacy_view(request):
    if request.method == 'POST':
        # Get the drug name from the form data
        drug_name = request.POST.get('drug')

        # Get the patient from the session
        patient = PatientInfo.objects.get(patient_national_code=request.session['patient_national_code'])

        # Get the drug from the pharmacy
        drug = Pharmacy.objects.get(drug_name=drug_name)

        # Check if the drug is in stock
        if drug.quantity > 0:
            # Decrease the drug quantity
            drug.quantity -= 1
            drug.save()

            # Check the patient's insurance status and add the appropriate message
            patient_health = PatientHealth.objects.get(patient=patient)
            if patient_health.insurance == 'yes':
                message = 'You have 70 percent discount as you have insurance.'
            else:
                message = 'You have to pay full price as you do not have insurance.'

            # Add the success message
            message += ' We have your drug in stock. Thanks for your shopping!'

            # Return a JsonResponse with the message
            return render(request, 'Pharmacy.html', {'message': message})
        else:
            # Return a JsonResponse with the error message
            return render(request, 'Pharmacy.html', {'message': f'Sorry, {drug_name} is currently out of stock.'})
    else:
        # Render the pharmacy page
        return render(request, 'Pharmacy.html')
def logout_view(request):
    logout(request)
    return redirect('main_page.html')


