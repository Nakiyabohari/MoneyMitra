from django.shortcuts import render, redirect
from .forms import MonthlyIncomeForm, MonthlySavingsForm


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