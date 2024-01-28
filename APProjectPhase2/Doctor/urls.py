from django.urls import path
from Doctor.views import views

urlpatterns = [
    path('enter_code/', views.enter_code, name='enter_code'),
    path('clinic_info/<int:clinic_id>/', views.select_each_clinic_info, name='clinic_info'),
    path('patient_info/<str:patient_national_code>/', views.select_each_patient_info, name='patient_info'),
]
