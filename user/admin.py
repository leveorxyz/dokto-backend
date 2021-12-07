from django.contrib import admin

from .models import (
    User,
    DoctorInfo,
    PatientInfo,
    PharmacyInfo,
    ClinicInfo,
    DoctorEducation,
)

# Register your models here.
models = [User, DoctorInfo, PatientInfo, PharmacyInfo, ClinicInfo, DoctorEducation]
for model in models:
    admin.site.register(model)
