from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Income_model
from .models import Expense_model,Category
from .models import Expensereport_model
from .models import Transaction_history_model
from .forms import addincome_Form
from .forms import add_expense_Form


# ==========================
# ADD INCOME
# ==========================
@login_required

@login_required
def addincome(request):

    if request.method == "POST":

        source = request.POST.get("income_source")
        amount = request.POST.get("amount")

        
        income = Income_model(
    user=request.user,
    income_source=source,
    amount=amount,
    payment_method=request.POST.get("payment_method"),
    notes=request.POST.get("notes")
)

        income.save()

        return redirect("dashboard")

    return render(request, "addincome.html")

# ==========================
# ADD EXPENSE
# ==========================
from django.contrib import messages

@login_required
def add__expense(request):

    categories = Category.objects.filter(type="expense")

    if request.method == "POST":

        amount = request.POST.get("expense_amount")
        category_id = request.POST.get("category")
        date = request.POST.get("date")
        payment_type = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        category = Category.objects.get(id=category_id)

        expense = Expense_model(
            user=request.user,
            expense_amount=amount,
            category=category,
            date=date,
            expense_payment_method=payment_type,
            notes=notes
        )

        expense.save()

        return redirect("expensereport")

    return render(request, "add_expense.html", {"categories": categories})
    
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

    # Calculate income percentage
    for income in incomes:
        income.percent = (income.amount / total_income * 100) if total_income > 0 else 0

    # Calculate expense percentage
    for expense in expenses:
        expense.percent = (expense.expense_amount / total_expense * 100) if total_expense > 0 else 0

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

# Nakiya's code

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from budget.models import Category, Expense


@login_required
def add_expense(request):

    categories = Category.objects.filter(
        user=request.user,
        type="expense"
    )

    if request.method == "POST":

        amount = request.POST.get("expense_amount")
        category_id = request.POST.get("category")
        date = request.POST.get("date")
        payment_type = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        category = Category.objects.get(id=category_id)

        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            date=date,
            payment_type=payment_type,
            notes=notes
        )

        return redirect("expensereport")

    return render(request, "add_expense.html", {"categories": categories})

# End of Nakiya's code@login_requiredfrom django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def transaction_history(request):

    incomes = Income_model.objects.all()
    expenses = Expense_model.objects.all()

    transactions = []

    for income in incomes:
        transactions.append({
            "type": "income",
            "title": income.income_source,
            "amount": income.amount,
            "date": "Income Added"
        })

    for expense in expenses:
        transactions.append({
            "type": "expense",
            "title": expense.category.name,
            "amount": expense.expense_amount,
            "date": str(expense.date)
        })

    print("TRANSACTIONS:", transactions)

    total_income = incomes.aggregate(total=Sum("amount"))["total"] or 0
    total_expense = expenses.aggregate(total=Sum("expense_amount"))["total"] or 0

    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
    }

    return render(request, "transactionhistory.html", context)