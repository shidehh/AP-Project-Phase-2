"""
URL configuration for APProjectPhase2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# myproject/urls.py
from django.urls import path, include

urlpatterns = [
    path('ClinicAppointmentPharmacy/', include('ClinicAppointmentPharmacy.urls')),
    path('Doctor/', include('Doctor.urls')),
    path('Patient/', include('Patient.urls')),
    path('Secretary/', include('Secretary.urls')),
    path('clinic/', include('Clinic.urls')),
    # Add more paths here for more apps
]
