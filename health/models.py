from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name



class Symptom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    intensity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='symptom_images/', blank=True, null=True)
    audio = models.FileField(upload_to='symptom_audio/', blank=True, null=True)




class MedicalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    diagnosis = models.CharField(max_length=255)
    treatment = models.TextField()
    doctor_notes = models.TextField()
    image = models.ImageField(upload_to='diagnosis_images/', blank=True, null=True)
    audio = models.FileField(upload_to='diagnosis_audio/', blank=True, null=True)



#class MedicationReminder(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    medication_name = models.CharField(max_length=100)
#    dosage = models.CharField(max_length=100)
#    intake_time = models.DateTimeField()
#   created_at = models.DateTimeField(auto_now_add=True)

class MedicationReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    intake_time = models.DateTimeField()



    def __str__(self):
        return f"{self.medication_name} - {self.intake_time}"


