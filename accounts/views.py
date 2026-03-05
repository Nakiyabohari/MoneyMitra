from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile

# HOME
def home(request):
    return render(request, 'welcome.html')


# REGISTER
def register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        occupation = request.POST.get('occupation')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            full_name=full_name,
            occupation=occupation
        )

        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')


# DASHBOARD
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    # Available balance calculation
    available_balance = profile.monthly_salary - profile.emi

    context = {
        'profile': profile,
        'available_balance': available_balance,
    }

    return render(request, 'dashboard.html', context)



#menu
@login_required
def menu(request):
    return render(request, 'menu.html')

# PROFILE
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


# EDIT PROFILE
@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get('phone')
        profile.gender = request.POST.get('gender')

        if request.FILES.get('profile_photo'):
            profile.profile_photo = request.FILES.get('profile_photo')

        profile.save()
        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('home')


# 🧮 CALCULATOR
@login_required
def calculator(request):
    return render(request, 'calculator.html')


# 📅 CALENDAR
@login_required
def calendar_view(request):
    return render(request, 'calendar.html')