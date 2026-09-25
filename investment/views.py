from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal
from django.db.models import Sum

# from openai import OpenAI

from .forms import InvestmentForm
from .models import InvestmentPlan

from accounts.models import Profile
from transactions.models import Income_model, Expense_model
from EMI.models import EmiManager
from budget.models import MonthlyIncome


# ==============================
# INVESTMENT PAGE
# ==============================
@login_required
def investment_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Salary
    income = MonthlyIncome.objects.filter(user=request.user).order_by('-month').first()
    salary = income.salary if income else 0

    # Income transactions
    incomes = Income_model.objects.filter(user=request.user)
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    # Expenses
    expenses = Expense_model.objects.filter(user=request.user)
    total_expense = expenses.aggregate(total=Sum('expense_amount'))['total'] or 0

    # EMI
    emis = EmiManager.objects.filter(user=request.user)
    total_emi = sum(emi.monthly_amount for emi in emis)

    # Investments
    investment_total = InvestmentPlan.objects.filter(
        user=request.user
    ).aggregate(total=Sum('monthly_amount'))['total'] or 0

    # Available balance
    available_balance = salary + total_income - total_expense - total_emi - investment_total

    # Suggestions
    suggest_20 = int(available_balance * Decimal('0.20'))
    suggest_30 = int(available_balance * Decimal('0.30'))
    suggest_50 = int(available_balance * Decimal('0.50'))

    # -----------------------------
    # SAVE PLAN
    # -----------------------------
    if request.method == "POST":
        investment_type = request.POST.get("investment_type")
        amount = request.POST.get("amount")

        InvestmentPlan.objects.update_or_create(
            user=request.user,
            investment_type=investment_type,
            defaults={"monthly_amount": amount}
        )

        messages.success(request, "Investment saved successfully!")
        return redirect("investment")

    context = {
        "profile": profile,
        "available_balance": available_balance,
        "suggest_20": suggest_20,
        "suggest_30": suggest_30,
        "suggest_50": suggest_50
    }

    return render(request, "investment.html", context)


# ==============================
# INVESTMENT DETAILS PAGE
# ==============================
@login_required
def investment_details(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    investments = InvestmentPlan.objects.filter(user=request.user)

    total_amount = sum(i.monthly_amount for i in investments)

    etf_amount = sum(
        i.monthly_amount for i in investments if i.investment_type == "ETFs"
    )

    mf_amount = sum(
        i.monthly_amount for i in investments if i.investment_type == "Mutual Funds"
    )

    etf_percent = (etf_amount / total_amount * 100) if total_amount > 0 else 0
    mf_percent = (mf_amount / total_amount * 100) if total_amount > 0 else 0

    context = {
        "profile": profile,
        "investments": investments,
        "total_amount": total_amount,
        "etf_amount": etf_amount,
        "mf_amount": mf_amount,
        "etf_percent": round(etf_percent),
        "mf_percent": round(mf_percent),
    }

    return render(request, "investment_details.html", context)


# ==============================
# MITRA AI VIEW
# ==============================
@login_required
def mitra_ai(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."})

    user_message = request.POST.get("message")

    if not user_message or user_message.strip() == "":
        return JsonResponse({"reply": "Ask me something 😊"})

    try:
        client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        system_prompt = """
        You are MoneyMitra AI, a financial assistant for Indian students.

        IMPORTANT RULES:
        - Use only the exact numbers provided by the user.
        - Never modify numbers.
        - If user says 900, it means 900 (NOT 9000).
        - Repeat investment values before giving advice.
        - Be accurate over creative.
        - Keep response clear and practical.
        - Currency is Indian Rupees (₹).
        - If information is incomplete, ask a follow-up question.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )

        ai_text = response.choices[0].message.content.strip()

        return JsonResponse({"reply": ai_text})

    except Exception as e:
        print("AI Error:", e)
        return JsonResponse({
            "reply": "Mitra AI is temporarily unavailable."
        })