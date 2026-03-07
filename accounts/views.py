from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from httpx import request
from .models import Profile
from datetime import date
from django.db.models import Sum
from budget.models import MonthlyIncome,SavingsGoal,Category
from investment.models import InvestmentPlan
from EMI.models import EmiManager
from budget.forms import CategoryForm
from transactions.forms import add_expense_Form



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
@login_required
def income(request):

    if request.method == "POST":
        salary = request.POST.get("salary")

        MonthlyIncome.objects.create(
            user=request.user,
            month=date.today(),
            salary=salary
        )

        return redirect("dashboard")

    return render(request, "income.html")


#Add income
def add_income(request):
    if request.method == "POST":
        salary = request.POST.get("salary")

        # save income here if you have model
        # example:
        # Income.objects.create(user=request.user, amount=salary)

        return redirect('dashboard')   # go to saving page

    return render(request, "income.html")


# DASHBOARD
@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    # fetch salary
    income = MonthlyIncome.objects.filter(user=request.user).order_by('-month').first()
    salary = income.salary if income else 0

    # fetch savings goals
    savings_goals = SavingsGoal.objects.filter(user=request.user)

    # calculate total savings
    total_savings = sum(goal.current_amount for goal in savings_goals)

    # EMI
    emis = EmiManager.objects.filter(user=request.user)
    total_emi = sum(emi.monthly_amount for emi in emis)

    # investment
    investment_total = InvestmentPlan.objects.filter(
        user=request.user
    ).aggregate(total=Sum('monthly_amount'))['total'] or 0

    print(InvestmentPlan.objects.filter(user=request.user).values())

    context = {
        'profile': profile,
        'salary': salary,
        'total_savings': total_savings,
        'total_emi': total_emi,
        'investment_total': investment_total
    }

    return render(request, 'dashboard.html', context)

#EMI Manager
@login_required
def emimanager(request):

    emis = EmiManager.objects.filter(user=request.user)

    context = {
        'emis': emis
    }
    return render(request, 'emimanager.html')

#Monthly Budget
@login_required
def MonthlyBudget(request):

    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

            return redirect('MonthlyBudget')

    else:
        form = CategoryForm()

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'MonthlyBudget.html', context)

#Budget Analysis
@login_required
def BudgetAnalysis(request):
    return render(request, 'BudgetAnalysis.html')

#transactionshistry
@login_required
def transactionhistory(request):
    return render(request, 'transactionhistory.html')

# Savings Goals
@login_required
def savings_goal(request):

    goals = SavingsGoal.objects.filter(user=request.user)

    context = {
        'goals': goals
    }

    return render(request, 'savings_goal.html', context)

#Expense Report
@login_required
def expense_report(request):
    return render(request, 'expense_report.html')

#Add Expense
from budget.models import Category
@login_required
def add_expense(request):

    categories = Category.objects.filter(user=request.user)

    context = {
        "categories": categories
    }

    return render(request, "add_expense.html", context)


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