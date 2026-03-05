from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import SavingsGoal
from .forms import MonthlyIncomeForm, MonthlySavingsForm,SavingsGoalForm


def monthly_income(request):
    if request.method == "POST":
        form = MonthlyIncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('savings')   # ✅ FIXED HERE
    else:
        form = MonthlyIncomeForm()

    return render(request, 'income.html', {'form': form})




def monthly_savings(request):
    if request.method == "POST":
        form = MonthlySavingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = MonthlySavingsForm()

    return render(request, 'saving.html', {'form': form})



# done by bappu

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

from django.http import JsonResponse
from .models import SavingsGoal


def add_money(request, goal_id, amount):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    goal.current_amount += amount
    goal.save()

    return JsonResponse({"success": True})


def delete_goal(request, goal_id):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    goal.delete()

    return JsonResponse({"success": True})
# Nakiya's Views 
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm
from .models import Category

from .models import Expense, Category, MonthlyIncome


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

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'MonthlyBudget.html', context)


# Budget Analysis starts here
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json

from .models import Expense, Category, MonthlyIncome


@login_required
def budget_analysis(request):

    user = request.user

    # =========================
    # CATEGORY WISE EXPENSE
    # =========================
    category_expense = (
        Expense.objects
        .filter(user=user)
        .values('category__id', 'category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # =========================
    # TOTAL EXPENSE
    # =========================
    total_expense = sum(item['total'] for item in category_expense) if category_expense else 0

    # =========================
    # TOTAL INCOME
    # =========================
    total_income = MonthlyIncome.objects.filter(user=user).aggregate(
        total=Sum('salary')
    )['total'] or 0


    # =========================
    # BUDGET VS SPENDING DATA
    # =========================
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


    # =========================
    # TOP SPENDING CATEGORIES
    # =========================
    top_categories = []

    if total_expense > 0:

        for item in category_expense:

            percent = (item['total'] / total_expense) * 100

            top_categories.append({
                "name": item['category__name'],
                "total": float(item['total']),
                "percent": round(percent, 1)
            })


    # =========================
    # CONTEXT
    # =========================
    context = {
        "labels": labels,
        "budget_data": budget_data,
        "spent_data": spent_data,
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "top_categories": top_categories
    }

    return render(request, "BudgetAnalysis.html", context)
#End of Nakiya's views

#start of chahat view for monthly summary
from django.shortcuts import render
from django.db.models import Sum
from .models import MonthlyIncome, MonthlySavings, Expense, Category
from EMI.models import EmiManager
from django.contrib.auth.decorators import login_required


@login_required
def monthly_summary(request):

    user = request.user

    # ==========================
    # TOTAL INCOME
    # ==========================
    total_income = MonthlyIncome.objects.filter(
        user=user
    ).aggregate(total=Sum('salary'))['total'] or 0

    # ==========================
    # SAVINGS
    # ==========================
    savings = MonthlySavings.objects.filter(
        user=user
    ).aggregate(total=Sum('amount'))['total'] or 0

    # ==========================
    # INVESTMENTS
    # ==========================
    investments = Category.objects.filter(
        user=user,
        type="investment"
    ).aggregate(total=Sum('budget_amount'))['total'] or 0

    # ==========================
    # EMI
    # ==========================
    emi = EmiManager.objects.aggregate(
        total=Sum('monthly_amount')
    )['total'] or 0

    # ==========================
    # EXPENSE
    # ==========================
    total_expense = Expense.objects.filter(
        user=user
    ).aggregate(total=Sum('amount'))['total'] or 0

    # ==========================
    # TOTAL DEDUCTIONS
    # ==========================
    total_deductions = savings + investments + emi

    # ==========================
    # AVAILABLE BALANCE
    # ==========================
    available_balance = total_income - total_deductions - total_expense

    # ==========================
    # DAILY LIMIT
    # ==========================
    daily_limit = available_balance / 30 if available_balance > 0 else 0

    context = {
        "total_income": total_income,
        "savings": savings,
        "investments": investments,
        "emi": emi,
        "deductions": total_deductions,
        "balance": available_balance,
        "daily": daily_limit,
    }

    return render(request, "monthly_summary.html", context)