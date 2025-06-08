from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-symptom/', views.add_symptom, name='add_symptom'),
    path('view-symptoms/', views.view_symptoms, name='view_symptoms'),
    path('add-diagnosis/', views.add_diagnosis, name='add_diagnosis'),
    path('view-diagnoses/', views.view_diagnoses, name='view_diagnoses'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-symptom/<int:symptom_id>/', views.delete_symptom, name='delete_symptom'),
    path('delete-diagnosis/<int:diagnosis_id>/', views.delete_diagnosis, name='delete_diagnosis'),
    path('add-reminder/', views.add_reminder, name='add_reminder'),
    path('view-reminders/', views.view_reminders, name='view_reminders'),




]
