from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import EmiManagerForm
from .models import EmiManager


# ==============================
# EMI LIST PAGE
# ==============================
@login_required
def emimanager(request):

    emi = EmiManager.objects.filter(user=request.user)

    total = emi.aggregate(
        Sum('monthly_amount')
    )['monthly_amount__sum']

    total = total if total else 0

    return render(request, 'emimanager.html', {
        'u': emi,
        'total': total
    })


# ==============================
# ADD EMI
# ==============================
from django.contrib import messages
from django.db.models import Sum
from budget.models import MonthlyIncome

@login_required
def addemi(request):

    monthly_income = MonthlyIncome.objects.filter(user=request.user).aggregate(
        total=Sum('salary')
    )['total']

    existing_emi = EmiManager.objects.filter(user=request.user).aggregate(
        total=Sum('monthly_amount')
    )['total'] or 0

    if request.method == 'POST':
        e = EmiManagerForm(request.POST)

        if e.is_valid():

            # ❌ NO INCOME CASE
            if not monthly_income:
                messages.error(request, "⚠️ Please add your monthly income first")
            
            else:
                new_emi = e.cleaned_data['monthly_amount']
                total_emi = existing_emi + new_emi

                # ❌ EMI > INCOME
                if total_emi > monthly_income:
                    deficit = total_emi - monthly_income

                    messages.error(
                        request,
                        f"⚠️ EMI exceeds income by ₹{deficit}"
                    )
                else:
                    # ✅ SAVE EMI
                    emi = e.save(commit=False)
                    emi.user = request.user
                    emi.save()

                    messages.success(request, "✅ EMI added successfully")
                    return redirect("emimanager")  # only success redirect

    else:
        e = EmiManagerForm()

    return render(request, 'addemi.html', {
        "e": e,
        "total": existing_emi
    })

# ==============================
# DELETE EMI (PERMANENT)
# ==============================
@login_required
def delete_emi(request, id):

    if request.method == "POST":
        emi = get_object_or_404(EmiManager, id=id, user=request.user)
        emi.delete()

    return redirect("emimanager")