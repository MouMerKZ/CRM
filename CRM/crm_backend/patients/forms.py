from django import forms
from .models import Patient, Appointment


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_of_birth': 'Дата рождения',
            'phone_number': 'Номер телефона',
            'iin': 'ИИН',
            'doctor': 'Доктор',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'ДД.ММ.ГГГГ'}),
        }

    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'doctor_name', 'notes', 'time']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }


class PatientSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search Patients')
