from django.urls import path
from Patient import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('clinic/<int:clinic_id>/', views.select_clinic_capacity_info, name='clinic_info'),
    path('patient/<str:patient_national_code>/', views.select_patient_reserved_appointments_info, name='patient_info'),
]
