from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Income_model
from .models import Expense_model
from .models import Expensereport_model
from .forms import addincome_Form
from .forms import add_expense_Form


# ==========================
# ADD INCOME
# ==========================
@login_required
def addincome(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        income_source = request.POST.get("income_source")
        payment_method = request.POST.get("payment_method")
        notes = request.POST.get("notes")

        Income_model.objects.create(
            user=request.user,
            amount=amount,
            income_source=income_source,
            payment_method=payment_method,
            notes=notes
        )

        return redirect("expensereport")

    return render(request, "addincome.html")


# ==========================
# ADD EXPENSE
# ==========================
@login_required
def add_expense(request):
    if request.method == "POST":
        expense_amount = request.POST.get("expense_amount")
        category = request.POST.get("category")
        custom_category = request.POST.get("custom_category")
        date = request.POST.get("date")
        expense_payment_method = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        if category == "custom" and custom_category:
            category = custom_category

        Expense_model.objects.create(
            user=request.user,
            expense_amount=expense_amount,
            category=category,
            date=date,
            expense_payment_method=expense_payment_method,
            notes=notes
        )

        return redirect("expensereport")

    return render(request, "add_expense.html")


# ==========================
# EXPENSE REPORT
# ==========================
@login_required
def expensereport(request):

    incomes = Income_model.objects.filter(user=request.user)
    expenses = Expense_model.objects.filter(user=request.user)

    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.expense_amount for e in expenses)

    balance = total_income - total_expense

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    years = list(range(2026, 2051))

    for income in incomes:
        if total_income > 0:
            income.percent = (income.amount / total_income) * 100
        else:
            income.percent = 0

    for expense in expenses:
        if total_expense > 0:
            expense.percent = (expense.expense_amount / total_expense) * 100
        else:
            expense.percent = 0

    total_transactions = incomes.count() + expenses.count()

    context = {
        "incomes": incomes,
        "expenses": expenses,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "months": months,
        "years": years,
        "total_transactions": total_transactions
    }

    return render(request, "expensereport.html", context)