from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date
from .models import SavingsGoal, Category, Expense, MonthlyIncome
from .forms import MonthlySavingsForm, SavingsGoalForm, CategoryForm
from EMI.models import EmiManager
from investment.models import InvestmentPlan


# =============================
# MONTHLY INCOME
# =============================
@login_required
def monthly_income(request):

    if request.method == "POST":
        salary = request.POST.get("salary")

        MonthlyIncome.objects.create(
            user=request.user,
            month=date.today(),
            salary=salary
        )

        return redirect('dashboard')

    return render(request, "income.html")


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
@login_required
def savings_goal(request):

    goals = SavingsGoal.objects.filter(user=request.user)

    total_saved = sum(g.current_amount for g in goals)
    total_target = sum(g.target_amount for g in goals)

    percent = 0
    if total_target > 0:
        percent = round((total_saved / total_target) * 100, 1)

    if request.method == "POST":

        form = SavingsGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()

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
def add_money(request, goal_id, amount):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    goal.current_amount += amount
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


# =============================
# BUDGET ANALYSIS
# =============================
@login_required
def budget_analysis(request):

    user = request.user

    category_expense = (
        Expense.objects
        .filter(user=user)
        .values('category__id', 'category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    total_expense = sum(item['total'] for item in category_expense) if category_expense else 0

    total_income = MonthlyIncome.objects.filter(user=user).aggregate(
        total=Sum('salary')
    )['total'] or 0

    categories = Category.objects.filter(user=user, type="expense")

    labels = []
    budget_data = []
    spent_data = []

    for cat in categories:

        spent = Expense.objects.filter(
            user=user,
            category_id=cat.id
        ).aggregate(total=Sum('amount'))['total'] or 0

        labels.append(cat.name)
        budget_data.append(float(cat.budget_amount or 0))
        spent_data.append(float(spent))

    return render(request, "BudgetAnalysis.html", {
        "labels": labels,
        "budget_data": budget_data,
        "spent_data": spent_data,
        "total_income": float(total_income),
        "total_expense": float(total_expense),
    })


# =============================
# MONTHLY SUMMARY
# =============================
from datetime import date, datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SavingsGoal, Expense, MonthlyIncome
from EMI.models import EmiManager
from investment.models import InvestmentPlan


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
    total_income = MonthlyIncome.objects.filter(
        user=user,
        month__year=year,
        month__month=month
    ).aggregate(total=Sum('salary'))['total'] or 0


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
    emi = EmiManager.objects.filter(
        user=user,
        start_date__year=year,
        start_date__month=month
    ).aggregate(total=Sum('monthly_amount'))['total'] or 0


    # =============================
    # EXPENSES
    # =============================
    total_expense = Expense.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    ).aggregate(total=Sum('amount'))['total'] or 0


    # =============================
    # CALCULATIONS
    # =============================
    total_deductions = savings + investments + emi

    available_balance = total_income - total_deductions - total_expense

    daily_limit = available_balance / 30 if available_balance > 0 else 0


    context = {
        "total_income": total_income,
        "savings": savings,
        "investments": investments,
        "emi": emi,
        "deductions": total_deductions,
        "balance": available_balance,
        "daily": daily_limit,
        "selected_month": selected_month
    }

    return render(request, "monthly_summary.html", context)