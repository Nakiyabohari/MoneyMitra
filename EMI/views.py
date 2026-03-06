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