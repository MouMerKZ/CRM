from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


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
            # If it's a new patient, increment the patient's count for the doctor
            self.doctor.patient_count += 1
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
