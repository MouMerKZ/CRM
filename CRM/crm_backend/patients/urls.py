from django.urls import path
from .views import patient_list, patient_create, patient_update, appointment_list, appointment_create, \
    appointment_update, generate_appointment_pdf, DoctorListView, financial_record_list, finance_record_create, \
    finance_record_update, finance_record_delete
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
    path('financial-records/create/', views.financial_record_create, name='financial_record_create'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('finance/', financial_record_list, name='finance_record_list'),
    path('financial-records/new/', finance_record_create, name='finance_record_create'),
    path('financial-records/<int:pk>/edit/', finance_record_update, name='finance_record_update'),
    path('financial-records/<int:pk>/delete/', finance_record_delete, name='finance_record_delete'),
    path('financial-records/report/', finance_record_report, name='finance_record_report'),
]
