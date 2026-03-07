from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Income_model
from .models import Expense_model,Category
from .models import Expensereport_model
from .models import Transaction_model
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

# def add__expense(request):
#     if request.method == "POST":
#         expense_amount = request.POST.get("expense_amount")
#         category = request.POST.get("category")
#         custom_category = request.POST.get("custom_category")
#         date = request.POST.get("date")
#         expense_payment_method = request.POST.get("expense_payment_method")
#         notes = request.POST.get("notes")

#         if category == "custom" and custom_category:
#             category = custom_category

#         Expense_model.objects.create(
#             expense_amount=expense_amount,
#             category=category,
#             date=date,
#             expense_payment_method=expense_payment_method,
#             notes=notes
#         )

#         return redirect("expensereport")

#     return render(request, "add_expense.html")



# ==========================
# ADD EXPENSE
# ==========================
@login_required
def add_expense(request):
    categories = Category.objects.all()  # filter by user if needed

    if request.method == "POST":
        expense_amount = request.POST.get("expense_amount")
        category_id = request.POST.get("category")
        custom_category_name = request.POST.get("custom_category")
        date = request.POST.get("date")
        expense_payment_method = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        if category_id == "custom" and custom_category_name:
            category = Category.objects.create(name=custom_category_name)
        else:
            category = Category.objects.filter(id=category_id).first()
            if not category:
                return redirect("add_expense")  # handle invalid category

        Expense_model.objects.create(
            user=request.user,
            expense_amount=expense_amount,
            category=category,
            date=date,
            expense_payment_method=expense_payment_method,
            notes=notes
        )
        return redirect("expensereport")

    return render(request, "add_expense.html", {"categories": categories})
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

def transactionhistory(request):

    transactions = Transaction_model.objects.all().order_by('-date')

    total_income = Transaction_model.objects.filter(type="income").aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction_model.objects.filter(type="expense").aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense
    }

    return render(request,"transactionhistory.html",context)
    return render(request, "expensereport.html", context)
