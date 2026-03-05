from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Income_model
from .models import Expense_model
from .models import Expensereport_model
from .forms import addincome_Form
from .forms import add_expense_Form
# Create your views here.

def addincome(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        income_source = request.POST.get("income_source")
        payment_method = request.POST.get("payment_method")
        notes = request.POST.get("notes")

        # ✅ SAVE TO DATABASE
        Income_model.objects.create(
            amount=amount,
            income_source=income_source,
            payment_method=payment_method,
            notes=notes
        )

        return redirect("expensereport")  # ✅ URL name

    return render(request, "addincome.html")

def add_expense(request):
    if request.method == "POST":
        expense_amount = request.POST.get("expense_amount")
        category = request.POST.get("category")
        date = request.POST.get("date")
        expense_payment_method = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        Expense_model.objects.create(
            expense_amount=expense_amount,
            category=category,
            date=date,
            expense_payment_method=expense_payment_method,
            notes=notes
        )

        return redirect("expensereport")

    return render(request, "add_expense.html")

# def expensereport(request):
#     incomes = Income_model.objects.all()
#     expenses = Expense_model.objects.all()

#     total_income = sum(i.amount for i in incomes)
#     total_expense = sum(e.expense_amount for e in expenses)
#     balance = total_income - total_expense

#     context = {
#         'incomes': incomes,
#         'expenses': expenses,
#         'total_income': total_income,
#         'total_expense': total_expense,
#         'balance': balance,
#     }

#     return render(request, 'expensereport.html', context)

def expensereport(request):
    incomes = Income_model.objects.all()
    expenses = Expense_model.objects.all()

    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.expense_amount for e in expenses)
    balance = total_income - total_expense

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    years = list(range(2026, 2051))

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

# End of Nakiya's code