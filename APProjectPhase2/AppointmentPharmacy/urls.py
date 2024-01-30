from django.urls import path

from AppointmentPharmacy.views import reserve_appointment,cancel_appointment,increase_capacity,check_patient

urlpatterns = [
    
    path('reserve_appointment/', reserve_appointment, name='reserve_appointment'),
    path('cancel_appointment/', cancel_appointment, name='cancel_appointment'),
    path('increase_capacity/', increase_capacity, name='increase_capacity'),
    path('pharmacy/', views.pharmacy_view, name='pharmacy_view'),
]
