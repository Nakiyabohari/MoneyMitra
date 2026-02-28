from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Income_model
from .models import Expense_model
from .models import Expensereport_model
# Create your views here.

def addincome(request):
    t =loader.get_template('addincome.html')
    return HttpResponse(t.render())


def add_expense(request):
    t =loader.get_template('add_expense.html')
    return HttpResponse(t.render())

def expensereport(request):
    t =loader.get_template('expensereport.html')
    return HttpResponse(t.render())
