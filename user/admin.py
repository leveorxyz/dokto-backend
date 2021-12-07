from django.contrib import admin

from .models import (
    User,
    DoctorInfo,
    PatientInfo,
    PharmacyInfo,
    ClinicInfo,
    DoctorEducation,
    DoctorExperience,
)

# Register your models here.
models = [
    User,
    DoctorInfo,
    PatientInfo,
    PharmacyInfo,
    ClinicInfo,
    DoctorEducation,
    DoctorExperience,
]
for model in models:
    admin.site.register(model)
