from django.contrib import admin
from .models import User, Symptom, MedicalHistory

admin.site.register(User)
admin.site.register(Symptom)
admin.site.register(MedicalHistory)
