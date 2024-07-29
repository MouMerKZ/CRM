from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils import timezone
from django import forms
from django.db import models


class FinancialRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES)

    def __str__(self):
        return f'{self.date} - {self.amount} - {self.description} - {self.record_type}'


class Budget(models.Model):
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    allocated_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.category}: {self.amount} allocated on {self.allocated_date}"


class CustomUser(AbstractUser):
    POSITION_CHOICES = [
        ('Doctor', 'Доктор'),
        ('Nurse', 'Медсестра'),
        ('Admin', 'Администратор'),
    ]

    CATEGORY_CHOICES = [
        ('Therapist', 'Терапевт'),
        ('Surgeon', 'Хирург'),
        ('Pediatrician', 'Педиатр'),
        # Добавьте другие категории, если необходимо
    ]

    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='Группы, к которым принадлежит этот пользователь.',
        verbose_name='группы'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Специфичные разрешения для этого пользователя.',
        verbose_name='разрешения пользователя'
    )

    def __str__(self):
        return self.username


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    iin = models.CharField(max_length=20, blank=True, null=True)
    doctor = models.ForeignKey(CustomUser, related_name='patients', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.doctor.save()
        super().save(*args, **kwargs)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField('Время встречи', blank=True, null=True)
    doctor_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.patient} - {self.date} {self.time}'


class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'amount', 'description', 'record_type']
