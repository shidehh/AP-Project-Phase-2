from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import Clinic
# Create your views here.
def update_from_api(request):
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:5000/slots')
        data = response.json()

        additional_info = {
            "1": {"service": "ophthalmology", "address": "Los Angeles; Beverly Hills", "contact": "09123758274"},
            "2": {"service": "gynecology", "address": "900 Pacific Ave, Everett", "contact": "09194726482"},
            "3": {"service": "otolaryngology", "address": "Harborview, 325 9th Ave, Seattle", "contact": "09185746253"},
            "4": {"service": "general", "address": "Hoyt Ave, Everett", "contact": "09109584726"},
            "5": {"service": "orthopedics", "address": "45th St, Seattle", "contact": "09108876543"},
            "6": {"service": "cardiology", "address": "Cleveland, Ohio", "contact": "09124837264"},
            "7": {"service": "dental", "address": "Alderwood Mall Blvd, Lynnwood", "contact": "09127564728"},
        }

        if data is not None:
            for clinic_id, capacity in data.items():
                info = additional_info.get(clinic_id, {})
                service = info.get("service", "")
                address = info.get("address", "")
                contact = info.get("contact", "")
                # in order to debuf or check, we can use clinic and created. not necessary
                clinic, created = Clinic.objects.update_or_create(
                    id=clinic_id,
                    defaults={
                        'capacity': capacity,
                        'service': service,
                        'address': address,
                        'clinic_contact_info': contact
                    }
                )

        return JsonResponse({"message": "Clinic capacities updated successfully."})
    else:
        return JsonResponse({"message": "Invalid request method."})