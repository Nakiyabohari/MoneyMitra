from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import EmiManagerForm
from .models import EmiManager


# ==============================
# EMI LIST PAGE
# ==============================
from datetime import date

@login_required
def emimanager(request):

    emis = EmiManager.objects.filter(user=request.user)

    emi_data = []

    for emi in emis:
        today = date.today()

        # total months
        total_months = emi.duration

        # months passed
        months_passed = (today.year - emi.start_date.year) * 12 + (today.month - emi.start_date.month)

        if months_passed < 0:
            months_passed = 0

        if months_passed > total_months:
            months_passed = total_months

        # months left
        months_left = total_months - months_passed

        # progress %
        progress = (months_passed / total_months) * 100 if total_months else 0

        # status
        status = "Completed" if months_left == 0 else "Active"

        emi_data.append({
            "obj": emi,
            "passed": months_passed,
            "left": months_left,
            "progress": progress,
            "status": status
        })

    total = emis.aggregate(Sum('monthly_amount'))['monthly_amount__sum'] or 0

    return render(request, 'emimanager.html', {
        'emis': emi_data,
        'total': total
    })

# ==============================
# ADD EMI
# ==============================
@login_required
def addemi(request):

    if request.method == 'POST':
        e = EmiManagerForm(request.POST)
        if e.is_valid():
            emi = e.save(commit=False)
            emi.user = request.user
            emi.save()
            return redirect("emimanager")
    else:
        e = EmiManagerForm()

    total = EmiManager.objects.filter(user=request.user).aggregate(
        Sum('monthly_amount')
    )['monthly_amount__sum']

    total = total if total else 0

    return render(request, 'addemi.html', {
        "e": e,
        "total": total
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