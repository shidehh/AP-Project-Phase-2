from django.urls import path
from . import views

urlpatterns = [
    path('enter_code/', views.enter_code, name='enter_code'),
    path('clinic_info/<int:clinic_id>/', views.select_each_clinic_info, name='select_each_clinic_info'),
    path('patient_info/<str:patient_national_code>/', views.select_each_patient_info, name='select_each_patient_info'),
]
