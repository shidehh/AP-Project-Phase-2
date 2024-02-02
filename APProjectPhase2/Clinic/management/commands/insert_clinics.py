from django.core.management.base import BaseCommand
from Clinic.models import Clinic

class Command(BaseCommand):
    help = 'Inserts clinic data into the database'

    def handle(self, *args, **options):
        clinics_data = {
            "1": {"capacity": 25, "service": "ophthalmology", "address": "Los Angeles; Beverly Hills", "clinic_contact_info": "09123758274"},
            "2": {"capacity": 15, "service": "gynecology", "address": "900 Pacific Ave, Everett", "clinic_contact_info": "09194726482"},
            "3": {"capacity": 15, "service": "otolaryngology", "address": "Harborview, 325 9th Ave, Seattle", "clinic_contact_info": "09185746253"},
            "4": {"capacity": 20, "service": "general", "address": "Hoyt Ave, Everett", "clinic_contact_info": "09109584726"},
            "5": {"capacity": 30, "service": "orthopedics", "address": "45th St, Seattle", "clinic_contact_info": "09108876543"},
            "6": {"capacity": 9, "service": "cardiology", "address": "Cleveland, Ohio", "clinic_contact_info": "09124837264"},
            "7": {"capacity": 8, "service": "dental", "address": "Alderwood Mall Blvd, Lynnwood", "clinic_contact_info": "09127564728"},
        }

        for clinic_id, data in clinics_data.items():
            Clinic.objects.update_or_create(
                clinic_id=clinic_id,
                defaults=data
            )

        self.stdout.write(self.style.SUCCESS('Successfully inserted clinic data'))
