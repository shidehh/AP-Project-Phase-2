from django.urls import path

from Clinic.views import update_from_api

urlpatterns = [
    path('update_from_api/', update_from_api, name='update_from_api'),
]
