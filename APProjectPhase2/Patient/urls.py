from django.urls import path
from Patient.views import sign_up,log_in,log_out,select_clinic_capacity_info,select_patient_reserved_appointments_info

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('clinic/<int:clinic_id>/', select_clinic_capacity_info, name='clinic_info'),
    path('patient/<str:patient_national_code>/', select_patient_reserved_appointments_info, name='patient_info'),
]
