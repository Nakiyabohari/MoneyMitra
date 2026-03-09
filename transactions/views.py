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
from .models import Income_model, Expense_model, Category, Expensereport_model, Transaction_history_model
from datetime import date



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
def add_expense(request):

    categories = Category.objects.filter(user=request.user, type="expense")

    if request.method == "POST":

        amount = request.POST.get("expense_amount")
        category_id = request.POST.get("category")
        expense_date = request.POST.get("date")
        payment_type = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        # CUSTOM CATEGORY
        if category_id == "custom":

            custom_name = request.POST.get("custom_category")

            if not custom_name:
                return render(request, "add_expense.html", {
                    "categories": categories,
                    "error": "Please enter custom category name"
                })

            category = Category.objects.create(
                user=request.user,
                name=custom_name,
                type="expense",
                month=date.today()
            )

        else:
            category = Category.objects.get(id=category_id)

        Expense_model.objects.create(
            user=request.user,
            expense_amount=amount,
            category=category,
            date=expense_date,
            expense_payment_method=payment_type,
            notes=notes
        )

        return redirect("dashboard")

    return render(request, "add_expense.html", {
        "categories": categories
    })




# ==========================
# EXPENSE REPORT
# ==========================
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def expensereport(request):

    user = request.user

    # =============================
    # GET SELECTED MONTH
    # =============================
    selected_month = request.GET.get("month")

    if selected_month:
        year, month = map(int, selected_month.split("-"))
    else:
        today = datetime.today()
        year = today.year
        month = today.month
        selected_month = f"{year}-{str(month).zfill(2)}"


    # =============================
    # FILTER DATA BY MONTH
    # =============================
    incomes = Income_model.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    expenses = Expense_model.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )


    # =============================
    # TOTAL CALCULATIONS
    # =============================
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.expense_amount for e in expenses)

    balance = total_income - total_expense


    # =============================
    # MONTHS (JAN-DEC)
    # =============================
    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]


    # =============================
    # CURRENT YEAR ONLY
    # =============================
    current_year = datetime.today().year
    years = [current_year]


    # =============================
    # INCOME PERCENT
    # =============================
    for income in incomes:
        income.percent = (income.amount / total_income * 100) if total_income > 0 else 0


    # =============================
    # EXPENSE PERCENT
    # =============================
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
        "total_transactions": total_transactions,
        "selected_month": selected_month
    }

    return render(request, "expensereport.html", context)

# # Nakiya's code

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


# @login_required
# def add_expense(request):

#     categories = Category.objects.filter(
#         user=request.user,
#         type="expense"
#     )

#     if request.method == "POST":

#         amount = request.POST.get("expense_amount")
#         category_id = request.POST.get("category")
#         date = request.POST.get("date")
#         payment_type = request.POST.get("expense_payment_method")
#         notes = request.POST.get("notes")

#         category = Category.objects.get(id=category_id)

#         Expense.objects.create(
#             user=request.user,
#             expense_amount=amount,
#             category=category,
#             amount=amount,
#             date=date,
#             payment_type=payment_type,
#             notes=notes

#         )

#         return redirect("expensereport")

#     return render(request, "add_expense.html", {"categories": categories})

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