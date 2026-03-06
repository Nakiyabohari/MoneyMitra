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
            return redirect('income')

    return render(request, 'login.html')

from django.shortcuts import render, redirect

#Income
def income(request):
    if request.method == "POST":
        salary = request.POST.get("salary")

        # save income here if you have model
        # example:
        # Income.objects.create(user=request.user, amount=salary)

        return redirect('dashboard')   # go to saving page

    return render(request, "income.html")


#Add income
def add_income(request):
    return render(request, "add_income.html")


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

#EMI Manager
@login_required
def emimanager(request):
    return render(request, 'emimanager.html')

#Monthly Budget
@login_required
def MonthlyBudget(request):
    return render(request, 'MonthlyBudget.html')

#Budget Analysis
@login_required
def BudgetAnalysis(request):
    return render(request, 'BudgetAnalysis.html')

#Savings Goals
@login_required
def savings_goal(request):
    return render(request, 'savings_goal.html')

#Expense Report
@login_required
def expense_report(request):
    return render(request, 'expense_report.html')

#Add Expense
@login_required
def add_expense(request):
    return render(request, 'add_expense.html')



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