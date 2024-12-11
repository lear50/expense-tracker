from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum


def expense_list(request):
    expenses = Expense.objects.all()

 
    category_filter = request.GET.get('category')
    if category_filter:
        expenses = expenses.filter(category=category_filter)

    
    date_filter = request.GET.get('date')
    if date_filter:
        expenses = expenses.filter(date=date_filter)

    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    categories = Expense.objects.values_list('category', flat=True).distinct()
    static_categories = ['Food', 'Transport', 'Utilities', 'Other']
    categories = list(set(categories) | set(static_categories)) 

    return render(request, 'tracker/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
        'total_amount': total_amount
    })

# Add new expense
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

# Update existing expense
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'tracker/add_expense.html', {'form': form, 'update': True})

# Delete an expense
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    
    return render(request, 'tracker/delete_expense.html', {'expense': expense})
