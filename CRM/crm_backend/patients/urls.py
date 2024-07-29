from django.urls import path
from .views import (
    patient_list, patient_create, patient_update, appointment_list, appointment_create,
    appointment_update, generate_appointment_pdf, DoctorListView, financial_record_list,
    financial_record_create, finance_record_update, finance_record_delete, finance_record_report,
    index, appointment_delete, generate_pdf, patient_delete
)
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/delete/<int:pk>/', views.patient_delete, name='patient_delete'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointments/pdf/', views.generate_appointment_pdf, name='generate_appointment_pdf'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('financial-records/', views.financial_record_list, name='finance_record_list'),
    path('financial-records/create/', views.financial_record_create, name='finance_record_create'),
    path('financial-records/<int:pk>/edit/', views.finance_record_update, name='finance_record_update'),
    path('financial-records/<int:pk>/delete/', views.finance_record_delete, name='finance_record_delete'),
    path('financial-records/report/', views.finance_record_report, name='finance_record_report'),
]
