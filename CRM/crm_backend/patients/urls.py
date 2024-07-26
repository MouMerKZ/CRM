from django.urls import path
from .views import patient_list, patient_create, patient_update, appointment_list, appointment_create, \
    appointment_update, generate_appointment_pdf, DoctorListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('patients/', patient_list, name='patient_list'),
    path('patients/add/', patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', patient_update, name='patient_update'),
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/add/', appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('patients/delete/<int:pk>/', views.patient_delete, name='patient_delete'),
    path('appointments/pdf/', generate_appointment_pdf, name='generate_appointment_pdf'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
]
