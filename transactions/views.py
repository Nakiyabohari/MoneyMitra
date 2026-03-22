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

from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def addincome(request):

    if request.method == "POST":

        source = request.POST.get("income_source")
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")
        notes = request.POST.get("notes")

        # ------------------------
        # VALIDATE AMOUNT
        # ------------------------
        try:
            amount = Decimal(amount)

            if amount <= 0:
                messages.error(request, "Amount must be greater than 0.")
                return render(request, "addincome.html")

            if amount > 10000000:
                messages.error(request, "Amount is too large.")
                return render(request, "addincome.html")

        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount.")
            return render(request, "addincome.html")

        # ------------------------
        # SAVE INCOME
        # ------------------------
        from datetime import datetime

        income_date = request.POST.get("date")
        income_date_obj = datetime.strptime(income_date, "%Y-%m-%d").date()

        income = Income_model(
            user=request.user,
            income_source=source,
            amount=amount,
            payment_method=payment_method,
            notes=notes,
            date=income_date_obj   # ✅ IMPORTANT
        )

        income.save()

        messages.success(request, "Income added successfully!")

        return redirect("dashboard")

    return render(request, "addincome.html")

    
# ==========================
# ADD EXPENSE
# ==========================
from django.contrib import messages
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from budget.models import MonthlyIncome   # ✅ ADD THIS IMPORT

@login_required
def add_expense(request):

    categories = Category.objects.filter(user=request.user, type="expense")

    if request.method == "POST":

        amount = request.POST.get("expense_amount")
        category_id = request.POST.get("category")
        expense_date = request.POST.get("date")
        payment_type = request.POST.get("expense_payment_method")
        notes = request.POST.get("notes")

        # -----------------------------
        # VALIDATE AMOUNT
        # -----------------------------
        try:
            amount = Decimal(amount)

            if amount <= 0:
                messages.error(request, "Amount must be greater than 0.")
                return render(request, "add_expense.html", {
                    "categories": categories
                })

            if amount > 10000000:
                messages.error(request, "Amount is too large.")
                return render(request, "add_expense.html", {
                    "categories": categories
                })

        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount value.")
            return render(request, "add_expense.html", {
                "categories": categories
            })

        # -----------------------------
        # VALIDATE DATE
        # -----------------------------
        expense_date_obj = datetime.strptime(expense_date, "%Y-%m-%d").date()

        if expense_date_obj > date.today():
            messages.error(request, "Future expense date is not allowed.")
            return render(request, "add_expense.html", {
                "categories": categories
            })

        # =====================================================
        # ✅ ADD THIS BLOCK HERE 🔥 (VERY IMPORTANT)
        # =====================================================
               # -----------------------------
        # ✅ CHECK INCOME (FIXED 🔥)
        # -----------------------------
        month_start = expense_date_obj.replace(day=1)

        income_exists = MonthlyIncome.objects.filter(
            user=request.user,
            month=month_start
        ).exists()

        if not income_exists:
            messages.error(
                request,
                "⚠️ Please add your income befor adding expenses."
            )
            return render(request, "add_expense.html", {
                "categories": categories
            })
        # =====================================================

        # -----------------------------
        # CUSTOM CATEGORY
        # -----------------------------
        if category_id == "custom":

            custom_name = request.POST.get("custom_category")

            if not custom_name:
                messages.error(request, "Please enter custom category name")
                return render(request, "add_expense.html", {
                    "categories": categories
                })

            category = Category.objects.create(
                user=request.user,
                name=custom_name,
                type="expense",
                month=date.today()
            )

        else:
            category = Category.objects.get(id=category_id)

        # -----------------------------
        # SAVE EXPENSE
        # -----------------------------
        Expense_model.objects.create(
            user=request.user,
            expense_amount=amount,
            category=category,
            date=expense_date_obj,
            expense_payment_method=payment_type,
            notes=notes
        )

        messages.success(request, "Expense added successfully!")
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

    incomes = Income_model.objects.filter(user=request.user)
    expenses = Expense_model.objects.filter(user=request.user)

    transactions = []

    for income in incomes:
        transactions.append({
            "id": income.id,
            "model": "income",
            "type": "income",
            "title": income.income_source,
            "amount": income.amount,
            "date": "Income Added"
        })

    for expense in expenses:
        transactions.append({
            "id": expense.id,
            "model": "expense",
            "type": "expense",
            "title": expense.category.name,
            "amount": expense.expense_amount,
            "date": str(expense.date)
        })

    total_income = incomes.aggregate(total=Sum("amount"))["total"] or 0
    total_expense = expenses.aggregate(total=Sum("expense_amount"))["total"] or 0

    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
    }

    return render(request, "transactionhistory.html", context)

from django.views.decorators.http import require_POST

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
@login_required
def delete_transaction(request):

    if request.method == "POST":

        transaction_id = request.POST.get("id")
        model = request.POST.get("model")

        if model == "income":
            Income_model.objects.filter(
                id=transaction_id,
                user=request.user
            ).delete()

        elif model == "expense":
            Expense_model.objects.filter(
                id=transaction_id,
                user=request.user
            ).delete()

        return JsonResponse({"status": "deleted"})

    return JsonResponse({"status": "error"})

@login_required
def edit_transaction(request):

    if request.method == "POST":

        id = request.POST.get("id")
        model = request.POST.get("model")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        notes = request.POST.get("notes")

        if model == "income":

            income = Income_model.objects.get(id=id,user=request.user)
            income.amount = amount
            income.income_source = category
            income.notes = notes
            income.save()

        elif model == "expense":

            expense = Expense_model.objects.get(id=id,user=request.user)
            expense.expense_amount = amount
            expense.notes = notes
            expense.save()

        return JsonResponse({"status":"success"})