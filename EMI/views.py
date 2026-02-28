from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import EmiManagerForm
from .models import EmiManager


# ==============================
# EMI LIST PAGE
# ==============================
def emimanager(request):

    emi = EmiManager.objects.all()

    total = EmiManager.objects.aggregate(
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
def addemi(request):

    if request.method == 'POST':
        e = EmiManagerForm(request.POST)
        if e.is_valid():
            e.save()
            return redirect("emimanager")
    else:
        e = EmiManagerForm()

    total = EmiManager.objects.aggregate(
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
from django.shortcuts import get_object_or_404

def delete_emi(request, id):
    if request.method == "POST":
        emi = get_object_or_404(EmiManager, id=id)
        emi.delete()
    return redirect("emimanager")