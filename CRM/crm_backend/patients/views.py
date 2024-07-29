from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, Appointment, CustomUser, FinancialRecord, Budget, FinancialRecord
from .forms import PatientForm, AppointmentForm, FinancialRecordForm, BudgetForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os
from django.views.generic import ListView
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import urllib, base64


def index(request):
    return render(request, 'patients/index.html')


@login_required
@permission_required('patients.can_view_patients', raise_exception=True)
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


def generate_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Determine the path to the font
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'fonts', 'Arial.ttf')
    pdfmetrics.registerFont(TTFont('Arial', font_path))

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Fetch patients from database
    patients = Patient.objects.all()

    # Prepare table data
    data = [['Имя', 'Фамилия', 'Дата рождения', 'Номер телефона', 'ИИН']]
    for patient in patients:
        data.append([
            patient.first_name,
            patient.last_name,
            patient.date_of_birth.strftime("%d.%m.%Y"),
            patient.phone_number if patient.phone_number else '',
            patient.iin if patient.iin else ''
        ])

    # Create the table
    table = Table(data)

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
    ])
    table.setStyle(style)

    # Build the PDF
    doc.build([table])

    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняет данные пациента в базу данных
            return redirect('patient_list')  # Перенаправляет на страницу списка пациентов
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})


def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
        else:
            print("Форма не валидна")
            print(form.errors)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form, 'patient': patient})


def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'patients/appointment_list.html', {'appointments': appointments})


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'patients/appointment_form.html', {'form': form})


def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'patients/appointment_form.html', {'form': form})


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'patients/appointment_confirm_delete.html', {'appointment': appointment})


def generate_appointment_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Determine the path to the font
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'fonts', 'Arial.ttf')
    pdfmetrics.registerFont(TTFont('Arial', font_path))

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Fetch appointments from database
    appointments = Appointment.objects.all()

    # Prepare table data
    data = [['Имя пациента', 'Дата встречи', 'Имя врача', 'Заметки']]
    for appointment in appointments:
        data.append([
            f'{appointment.patient.first_name} {appointment.patient.last_name}',
            appointment.date.strftime("%d.%m.%Y %H:%М"),
            appointment.doctor_name,
            appointment.notes if appointment.notes else ''
        ])

    # Create the table
    table = Table(data)

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
    ])
    table.setStyle(style)

    # Build the PDF
    doc.build([table])

    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


class DoctorListView(ListView):
    model = CustomUser
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return CustomUser.objects.filter(position='Doctor').annotate(patient_count=Count('patients'))


def financial_record_list(request):
    records = FinancialRecord.objects.all()
    return render(request, 'finances/financial_record_list.html', {'records': records})


def financial_record_create(request):
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financial_record_list')
    else:
        form = FinancialRecordForm()
    return render(request, 'finances/financial_record_form.html', {'form': form})

def financial_record_create(request):
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance_record_list')
    else:
        form = FinancialRecordForm()
    return render(request, 'finances/financial_record_form.html', {'form': form})


# Редактирование финансовой записи
def finance_record_update(request, pk):
    record = get_object_or_404(FinancialRecord, pk=pk)
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('finance_record_list')
    else:
        form = FinancialRecordForm(instance=record)
    return render(request, 'finances/financial_record_form.html', {'form': form, 'record': record})


# Удаление финансовой записи
def finance_record_delete(request, pk):
    record = get_object_or_404(FinancialRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('finance_record_list')
    return render(request, 'finances/financial_record_form.html', {'record': record})


def finance_record_report(request):
    records = FinancialRecord.objects.all()
    dates = [record.date for record in records]
    amounts = [record.amount for record in records]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts)
    plt.title('Финансовые записи')
    plt.xlabel('Дата')
    plt.ylabel('Сумма')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'finances/financial_record_form.html', {'data': uri})
