from django.urls import path
from AppointmentPharmacy.views import reserve_appointment, cancel_appointment, increase_capacity, pharmacy_view,logout_view

# In Django URL patterns, '<str:user_type>/' is a dynamic part of the URL.
# 'str' indicates that this part of the URL should be interpreted as a string.
# 'user_type' is the variable name that will be passed to the view function.
# For example, if the URL is '/reserve_appointment/patient/', 
# the view function will receive 'patient' as the value of 'user_type'.

urlpatterns = [
    path('reserve_appointment/<str:user_type>/', reserve_appointment, name='reserve_appointment'),
    path('cancel_appointment/<str:user_type>/', cancel_appointment, name='cancel_appointment'),
    path('increase_capacity/', increase_capacity, name='increase_capacity'),
    path('pharmacy/', pharmacy_view, name='pharmacy_view'),
    path('logout/', logout_view, name='logout'),
]
