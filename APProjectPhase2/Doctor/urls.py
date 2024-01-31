from django.urls import path
from Doctor.views import enter_code, select_each_clinic_info, select_each_patient_info

urlpatterns = [
    path('enter_code/', enter_code, name='enter_code'),
    path('clinic_info/<int:clinic_id>/', select_each_clinic_info, name='select_each_clinic_info'),
    path('patient_info/<str:patient_national_code>/', select_each_patient_info, name='select_each_patient_info'),
]
