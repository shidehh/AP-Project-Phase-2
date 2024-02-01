from django.urls import path
from Secretary.views import enter_code,select_each_clinic_info,logout_view

urlpatterns = [
    path('enter_code/', enter_code, name='enter_code'),
    path('clinic_info/<int:clinic_id>/', select_each_clinic_info, name='select_each_clinic_info'),
    '''path('logout/', logout_view, name='logout'),'''
]
