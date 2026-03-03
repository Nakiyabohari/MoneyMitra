from django.shortcuts import render, redirect
from .forms import MonthlyIncomeForm, MonthlySavingsForm


def monthly_income(request):
    if request.method == "POST":
        form = MonthlyIncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('savings')   # ✅ FIXED HERE
    else:
        form = MonthlyIncomeForm()

    return render(request, 'income.html', {'form': form})


def monthly_savings(request):
    if request.method == "POST":
        form = MonthlySavingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = MonthlySavingsForm()

    return render(request, 'saving.html', {'form': form})