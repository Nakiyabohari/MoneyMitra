from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from decimal import Decimal
from django.db.models import Sum

from accounts.models import Profile
from transactions.models import Income_model, Expense_model
from EMI.models import EmiManager
from .models import InvestmentPlan
from budget.models import MonthlyIncome

from openai import OpenAI


# ==============================
# INVESTMENT PAGE
# ==============================

@login_required
def investment_view(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    # salary
    income = MonthlyIncome.objects.filter(user=request.user).order_by('-month').first()
    salary = income.salary if income else 0

    # income transactions
    incomes = Income_model.objects.filter(user=request.user)
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    # expenses
    expenses = Expense_model.objects.filter(user=request.user)
    total_expense = expenses.aggregate(total=Sum('expense_amount'))['total'] or 0

    # EMI
    emis = EmiManager.objects.filter(user=request.user)
    total_emi = sum(emi.monthly_amount for emi in emis)

    # investments
    investment_total = InvestmentPlan.objects.filter(
        user=request.user
    ).aggregate(total=Sum('monthly_amount'))['total'] or 0

    # available balance
    available_balance = salary + total_income - total_expense - total_emi - investment_total

    # suggestions
    suggest_20 = int(available_balance * Decimal('0.20'))
    suggest_30 = int(available_balance * Decimal('0.30'))
    suggest_50 = int(available_balance * Decimal('0.50'))

    # ==============================
    # POST (SAVE INVESTMENT)
    # ==============================
    if request.method == "POST":

        investment_type = request.POST.get("investment_type")
        amount = request.POST.get("amount")

        # 🔥 CHECK INCOME FIRST
        today = date.today()
        month_start = today.replace(day=1)

        income_exists = MonthlyIncome.objects.filter(
            user=request.user,
            month=month_start
        ).exists()

        if not income_exists:
            messages.error(
                request,
                "⚠️ Please add your income before making investments."
            )
            return render(request, "investment.html", {
                "available_balance": available_balance,
                "suggest_20": suggest_20,
                "suggest_30": suggest_30,
                "suggest_50": suggest_50
            })

        # SAVE INVESTMENT
        InvestmentPlan.objects.update_or_create(
            user=request.user,
            investment_type=investment_type,
            defaults={"monthly_amount": amount}
        )

        messages.success(request, "Investment saved successfully!")
        return redirect("investment")

    # ==============================
    # GET REQUEST
    # ==============================
    context = {
        "available_balance": available_balance,
        "suggest_20": suggest_20,
        "suggest_30": suggest_30,
        "suggest_50": suggest_50
    }

    return render(request, "investment.html", context)


# ==============================
# INVESTMENT DETAILS
# ==============================

@login_required
def investment_details(request):

    investments = InvestmentPlan.objects.filter(user=request.user)

    total_amount = sum(i.monthly_amount for i in investments)

    etf_amount = sum(i.monthly_amount for i in investments if i.investment_type == "ETFs")
    mf_amount = sum(i.monthly_amount for i in investments if i.investment_type == "Mutual Funds")

    etf_percent = (etf_amount / total_amount * 100) if total_amount > 0 else 0
    mf_percent = (mf_amount / total_amount * 100) if total_amount > 0 else 0

    context = {
        "investments": investments,
        "total_amount": total_amount,
        "etf_amount": etf_amount,
        "mf_amount": mf_amount,
        "etf_percent": round(etf_percent),
        "mf_percent": round(mf_percent),
    }

    return render(request, "investment_details.html", context)


# ==============================
# MITRA AI
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