from calendar import month
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date

from httpx import request
from .models import SavingsGoal, Category, Expense, MonthlyIncome
from .forms import MonthlySavingsForm, SavingsGoalForm, CategoryForm
from EMI.models import EmiManager
from investment.models import InvestmentPlan
from budget.models import Category
from transactions.models import Income_model
from .models import Category
from budget.models import Expense

# =============================
# MONTHLY INCOME
# =============================
@login_required
def income(request):

    income_obj = MonthlyIncome.objects.filter(user=request.user).first()

    if request.method == "POST":
        salary = request.POST.get("salary")

        print("SALARY RECEIVED:", salary)  # 🔥 DEBUG

        MonthlyIncome.objects.update_or_create(
            user=request.user,
            defaults={
                "salary": salary,
                "month": date.today()
            }
        )

        return redirect("dashboard")

    return render(request, "income.html", {
        "income": income_obj
    })
# =============================
# MONTHLY SAVINGS
# =============================
@login_required
def monthly_savings(request):

    if request.method == "POST":

        form = MonthlySavingsForm(request.POST)

        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.month = date.today()
            saving.save()

            return redirect('success')

    else:
        form = MonthlySavingsForm()

    return render(request, 'saving.html', {'form': form})


# =============================
# SAVINGS GOAL
# =============================
from django.contrib import messages
from django.db.models import Sum

@login_required
def savings_goal(request):

    goals = SavingsGoal.objects.filter(user=request.user)

    total_saved = sum(g.current_amount for g in goals)
    total_target = sum(g.target_amount for g in goals)

    percent = 0
    if total_target > 0:
        percent = round((total_saved / total_target) * 100, 1)

    # 👉 CHECK ONLY SALARY
    monthly_income = MonthlyIncome.objects.filter(user=request.user).aggregate(
        total=Sum('salary')
    )['total'] or 0

    if request.method == "POST":

        form = SavingsGoalForm(request.POST)

        if form.is_valid():

            # ❌ NO SALARY
            if monthly_income == 0:
                messages.error(request, "Please add your income first")

            else:
                goal = form.save(commit=False)
                goal.user = request.user
                goal.save()

                messages.success(request, "Goal created successfully ✅")
                return redirect("savings_goal")

    else:
        form = SavingsGoalForm()

    return render(request, "savings_goal.html", {
        "form": form,
        "goals": goals,
        "total_saved": total_saved,
        "total_target": total_target,
        "total_percent": percent
    })


# =============================
# ADD MONEY
# =============================
from decimal import Decimal
from django.http import JsonResponse

def add_money(request, goal_id, amount):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    amount = Decimal(amount)

    remaining = goal.target_amount - goal.current_amount

    # prevent exceeding target
    if amount > remaining:
        amount = remaining

    goal.current_amount += amount
    goal.save()

    return JsonResponse({"success": True})

from decimal import Decimal
from django.http import JsonResponse

def remove_money(request, goal_id, amount):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    amount = Decimal(amount)

    goal.current_amount -= amount

    # prevent negative savings
    if goal.current_amount < 0:
        goal.current_amount = 0

    goal.save()

    return JsonResponse({"success": True})


# =============================
# DELETE GOAL
# =============================
def delete_goal(request, goal_id):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    goal.delete()

    return JsonResponse({"success": True})


# =============================
# MONTHLY BUDGET
# =============================
@login_required
def monthly_budget(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            category = form.save(commit=False)

            if form.cleaned_data['name'] == "Custom":
                custom_name = form.cleaned_data.get('custom_name')

                if custom_name:
                    category.name = custom_name

            category.user = request.user
            category.type = "expense"
            category.save()

            return redirect('monthly_budget')

    else:
        form = CategoryForm()

    categories = Category.objects.filter(
        user=request.user,
        type='expense'
    )

    return render(request, 'MonthlyBudget.html', {
        'form': form,
        'categories': categories
    })
    



from django.http import JsonResponse
from .models import Category   # use your actual model


def delete_budget(request, id):

    if request.method == "POST":

        budget = Category.objects.get(id=id)
        budget.delete()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})



import json
from django.views.decorators.csrf import csrf_exempt

def edit_budget(request, id):

    if request.method == "POST":

        data = json.loads(request.body)

        amount = data.get("amount")

        budget = Category.objects.get(id=id)
        budget.budget_amount = amount
        budget.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


# =============================
# BUDGET ANALYSIS
# =============================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from transactions.models import Expense_model, Income_model


@login_required
def budget_analysis(request):

    # USER DATA
    incomes = Income_model.objects.filter(user=request.user)
    expenses = Expense_model.objects.filter(user=request.user)

    # TOTALS
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.expense_amount for e in expenses)

    # CATEGORY TOTALS
    category_expense = (
        Expense_model.objects
        .filter(user=request.user)
        .values("category__name")
        .annotate(total=Sum("expense_amount"))
        .order_by("-total")
    )

    labels = []
    spent_data = []
    budget_data = []

    for item in category_expense:
        labels.append(item["category__name"])
        spent_data.append(float(item["total"]))
        budget_data.append(0)

    # TOP SPENDING
    top_categories = []

    for item in category_expense:

        percent = 0
        if total_expense > 0:
            percent = round((item["total"] / total_expense) * 100, 1)

        top_categories.append({
            "name": item["category__name"],
            "total": float(item["total"]),
            "percent": percent
        })

    context = {
        "labels": labels,
        "budget_data": budget_data,
        "spent_data": spent_data,
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "top_categories": top_categories
    }

    return render(request, "BudgetAnalysis.html", context)



# =============================
# MONTHLY SUMMARY
# =============================
from datetime import date, datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SavingsGoal, MonthlyIncome
from EMI.models import EmiManager
from investment.models import InvestmentPlan
from transactions.models import Expense_model
from transactions.models import Income_model

@login_required
def monthly_summary(request):

    user = request.user

    selected_month = request.GET.get("month")

    # =============================
    # GET SELECTED MONTH
    # =============================
    if selected_month:
        year, month = map(int, selected_month.split("-"))
    else:
        today = datetime.today()
        year = today.year
        month = today.month
        selected_month = f"{year}-{str(month).zfill(2)}"

# =============================
# TOTAL INCOME
# =============================
    salary_income = MonthlyIncome.objects.filter(
    user=user,
    month__year=year,
    month__month=month
    ).aggregate(total=Sum('salary'))['total'] or 0

    transaction_income = Income_model.objects.filter(
    user=user,
    date__year=year,
    date__month=month
    ).aggregate(total=Sum('amount'))['total'] or 0


    total_income = salary_income + transaction_income

    
    
    # =============================
    # SAVINGS (ONLY CURRENT MONTH)
    # =============================
    today = date.today()

    if year == today.year and month == today.month:
        savings = SavingsGoal.objects.filter(
            user=user
        ).aggregate(total=Sum('current_amount'))['total'] or 0
    else:
        savings = 0


    # =============================
    # INVESTMENTS
    # =============================
    investments = InvestmentPlan.objects.filter(
        user=user,
        created_at__year=year,
        created_at__month=month
    ).aggregate(total=Sum('monthly_amount'))['total'] or 0


    # =============================
    # EMI
    # =============================
    from dateutil.relativedelta import relativedelta

    current_month_date = date(year, month, 1)

    all_emis = EmiManager.objects.filter(user=user)

    total_emi = 0

    for emi_obj in all_emis:
        start = emi_obj.start_date.replace(day=1)
        duration = emi_obj.duration

        end = start + relativedelta(months=duration)

        if start <= current_month_date < end:
            total_emi += emi_obj.monthly_amount

    emi = total_emi


    # =============================
    # EXPENSES
    # =============================
    total_expense = Expense_model.objects.filter(
    user=user,
    date__year=year,
    date__month=month
    ).aggregate(total=Sum('expense_amount'))['total'] or 0


    # =============================
    # CALCULATIONS
    # =============================
    total_deductions = savings + investments + emi + total_expense

    available_balance = total_income - total_deductions

    daily_limit = available_balance / 30 if available_balance > 0 else 0


    context = {
        "total_income": total_income,
        "savings": savings,
        "expense": total_expense,
        "investments": investments,
        "emi": emi,
        "deductions": total_deductions,
        "balance": available_balance,
        "daily": daily_limit,
        "selected_month": selected_month
    }

    return render(request, "monthly_summary.html", context)