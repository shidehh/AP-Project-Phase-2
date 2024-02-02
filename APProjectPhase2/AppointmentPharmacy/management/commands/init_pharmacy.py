from django.core.management.base import BaseCommand
from AppointmentPharmacy.models import Pharmacy

class Command(BaseCommand):
    help = 'Initialize Pharmacy model'

    def handle(self, *args, **options):
        inventory = {
            'Tetrahydrozoline': 25,
            'carbetocin': 15,
            'Mometasone': 15,
            'Amoxicillin': 20,
            'Diclofenac': 30,
            'Amiodarone': 9,
            'Articaine': 8
        }

        for drug_name, quantity in inventory.items():
            Pharmacy.objects.update_or_create(
                drug_name=drug_name,
                defaults={'quantity': quantity}
            )

        self.stdout.write(self.style.SUCCESS('Successfully initialized Pharmacy model'))
