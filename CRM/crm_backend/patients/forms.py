from django import forms
from .models import Patient, Appointment, CustomUser, FinancialRecord, Budget


class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ['record_type', 'amount', 'description', 'date']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'allocated_date']


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


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'position', 'category', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'position': 'Должность',
            'category': 'Категория',
            'password': 'Пароль',
        }
