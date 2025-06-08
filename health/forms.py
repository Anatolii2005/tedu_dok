from django import forms
from .models import User
from .models import Symptom, MedicalHistory
from .models import MedicationReminder


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'phone', 'password']

class LoginForm(forms.Form):
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)




class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['title', 'intensity', 'description', 'image', 'audio']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'treatment', 'doctor_notes', 'image', 'audio']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'doctor_notes': forms.Textarea(attrs={'rows': 2}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone']



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)


class MedicationReminderForm(forms.ModelForm):
    class Meta:
        model = MedicationReminder
        fields = ['medication_name', 'dosage', 'intake_time']
        widgets = {
            'intake_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


