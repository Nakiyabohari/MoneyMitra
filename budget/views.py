from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import SavingsGoal
from .forms import MonthlyIncomeForm, MonthlySavingsForm,SavingsGoalForm


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



# done by bappu

@login_required
def savings_goal(request):
    goals = SavingsGoal.objects.filter(user=request.user)

    total_saved = sum(g.current_amount for g in goals)
    total_target = sum(g.target_amount for g in goals)

    percent = 0
    if total_target > 0:
        percent = round((total_saved / total_target) * 100, 1)

    if request.method == "POST":
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("savings_goal")
    else:
        form = SavingsGoalForm()

    return render(request, "savings_goal.html", {
        "form": form,
        "goals": goals,
        "total_saved": total_saved,
        "total_target": total_target,
        "total_percent": percent
    })

from django.http import JsonResponse
from .models import SavingsGoal


def add_money(request, goal_id, amount):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    goal.current_amount += amount
    goal.save()

    return JsonResponse({"success": True})


def delete_goal(request, goal_id):

    goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

    goal.delete()

    return JsonResponse({"success": True})