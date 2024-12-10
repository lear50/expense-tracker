from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),  # List expenses
    path('add/', views.add_expense, name='add_expense'),  # Add new expense
    path('update/<int:expense_id>/', views.update_expense, name='update_expense'),  # Update existing expense
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # Delete expense
]
