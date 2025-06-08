from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm, LoginForm, ProfileForm, ChangePasswordForm
from django.contrib import messages
from .forms import SymptomForm, MedicalHistoryForm
from .models import Symptom, MedicalHistory
from .forms import MedicationReminderForm
from django.utils import timezone
from .forms import MedicationReminderForm
from .models import MedicationReminder
from .models import MedicationReminder
from django.shortcuts import render, redirect




# РЕГИСТРАЦИЯ
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(phone=form.cleaned_data['phone']).exists():
                messages.error(request, "Пользователь с таким номером уже существует.")
            else:
                user = form.save(commit=False)
                from django.contrib.auth.hashers import make_password
                user.password = make_password(user.password)
                user.save()
                messages.success(request, "Регистрация успешна. Теперь войдите.")
                return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# АВТОРИЗАЦИЯ
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(phone=phone)
                from django.contrib.auth.hashers import check_password
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('dashboard')
                else:
                    messages.error(request, "Неверный пароль.")
            except User.DoesNotExist:
                messages.error(request, "Пользователь не найден.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# ВЫХОД
def logout_view(request):
    request.session.flush()
    return redirect('login')

# ГЛАВНАЯ (после входа)
def dashboard(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if not user_id:
        return redirect('login')
    return render(request, 'dashboard.html', {'user_name': user_name})





# Добавление симптома
def add_symptom(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.user_id = request.session['user_id']
            symptom.save()
            return redirect('view_symptoms')
    else:
        form = SymptomForm()
    return render(request, 'add_symptom.html', {'form': form})

# Просмотр симптомов
def view_symptoms(request):
    if not request.session.get('user_id'):
        return redirect('login')
    symptoms = Symptom.objects.filter(user_id=request.session['user_id']).order_by('-date')
    return render(request, 'view_symptoms.html', {'symptoms': symptoms})

# Добавление диагноза
def add_diagnosis(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            diag = form.save(commit=False)
            diag.user_id = request.session['user_id']
            diag.save()
            return redirect('view_diagnoses')
    else:
        form = MedicalHistoryForm()
    return render(request, 'add_diagnosis.html', {'form': form})

# Просмотр истории болезней
def view_diagnoses(request):
    if not request.session.get('user_id'):
        return redirect('login')
    history = MedicalHistory.objects.filter(user_id=request.session['user_id']).order_by('-date')
    return render(request, 'view_diagnoses.html', {'history': history})




#Профиль
def profile_view(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            request.session['user_name'] = form.cleaned_data['name']
            messages.success(request, "Профиль обновлен.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})

#Смена пороля 
def change_password(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            from django.contrib.auth.hashers import check_password, make_password
            if not check_password(form.cleaned_data['old_password'], user.password):
                messages.error(request, "Старый пароль неверен.")
            else:
                user.password = make_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, "Пароль обновлён.")
                return redirect('profile')
    else:
        form = ChangePasswordForm()

    return render(request, 'change_password.html', {'form': form})



from django.shortcuts import get_object_or_404

# Удалить симптом
def delete_symptom(request, symptom_id):
    if not request.session.get('user_id'):
        return redirect('login')
    symptom = get_object_or_404(Symptom, id=symptom_id, user_id=request.session['user_id'])
    symptom.delete()
    return redirect('view_symptoms')

# Удалить диагноз
def delete_diagnosis(request, diagnosis_id):
    if not request.session.get('user_id'):
        return redirect('login')
    diag = get_object_or_404(MedicalHistory, id=diagnosis_id, user_id=request.session['user_id'])
    diag.delete()
    return redirect('view_diagnoses')



def add_reminder(request):
    # Проверка: пользователь вошёл?
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == 'POST':
        form = MedicationReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user_id = request.session['user_id']  # Привязка к пользователю
            reminder.save()
            return redirect('view_reminders')
    else:
        form = MedicationReminderForm()

    return render(request, 'add_reminder.html', {'form': form})


from django.shortcuts import render
from .models import MedicationReminder

def view_reminders(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    reminders = MedicationReminder.objects.filter(user_id=request.session['user_id']).order_by('intake_time')
    
    return render(request, 'view_reminders.html', {'reminders': reminders})





