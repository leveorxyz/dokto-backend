from django.contrib import admin

from .models import User, DoctorInfo, PatientInfo, PharmacyInfo, ClinicInfo

# Register your models here.
models = [User, DoctorInfo, PatientInfo, PharmacyInfo, ClinicInfo]
for model in models:
    admin.site.register(model)
