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


# Nakiya's Views 
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm
from .models import Category


@login_required
def monthly_budget(request):

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():

            category = form.save(commit=False)

            if form.cleaned_data['name'] == "Custom":
                custom_name = form.cleaned_data.get('custom_name')

                if custom_name:
                    category.name = custom_name

            category.user = request.user
            category.type = "expense"
            category.save()

            return redirect('monthly_budget')

    else:
        form = CategoryForm()

    categories = Category.objects.filter(
        user=request.user,
        type='expense'
    )

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'MonthlyBudget.html', context)

#End of Nakiya's views