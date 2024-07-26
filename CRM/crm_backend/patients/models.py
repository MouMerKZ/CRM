from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Patient, Appointment

class CustomUser(AbstractUser):
    position = models.CharField(max_length=100, blank=True, null=True, default='Doctor')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Patient(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('Дата рождения')
    phone_number = models.CharField('Номер телефона', max_length=20, blank=True, null=True)
    iin = models.CharField('ИИН', max_length=12, blank=True, null=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField('Время встречи', blank=True, null=True)
    doctor_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.patient} - {self.date} {self.time}'


