import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpenseTracker.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import Budget, Addmoney_info

def setup_sample_data():
    try:
        # Get the first user (assuming this is your user)
        user = User.objects.first()
        if not user:
            print("No users found in the database. Please create a user first.")
            return

        # Sample budget categories and amounts
        budgets = [
            ('Food & Groceries', 5000),
            ('Shopping', 3000),
            ('Rent', 10000),
            ('Transportation', 2000),
            ('Entertainment', 1500),
        ]

        # Create budgets
        for category, amount in budgets:
            Budget.objects.get_or_create(
                user=user,
                category=category,
                defaults={'amount': amount}
            )
            print(f"Created/Updated budget for {category}: ₹{amount}")

        # Sample expenses for the current month
        current_month = datetime.date.today()
        expenses = [
            ('Food & Groceries', 3500, current_month - datetime.timedelta(days=5)),
            ('Shopping', 2800, current_month - datetime.timedelta(days=3)),
            ('Rent', 10000, current_month - datetime.timedelta(days=1)),
            ('Transportation', 1200, current_month - datetime.timedelta(days=2)),
            ('Entertainment', 1000, current_month - datetime.timedelta(days=4)),
        ]

        # Create expenses
        for category, amount, date in expenses:
            Addmoney_info.objects.create(
                user=user,
                Category=category,
                Date=date,
                add_money='Expense',
                quantity=amount
            )
            print(f"Added expense for {category}: ₹{amount} on {date}")

        print("\nSample data setup completed successfully!")
        print("\nBudget Progress Overview:")
        for budget in Budget.objects.filter(user=user):
            spent = Addmoney_info.objects.filter(
                user=user,
                Category=budget.category,
                add_money='Expense',
                Date__month=current_month.month
            ).aggregate(django.db.models.Sum('quantity'))['quantity__sum'] or 0
            print(f"{budget.category}: Spent ₹{spent} of ₹{budget.amount} ({(spent/budget.amount*100):.1f}%)")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    setup_sample_data() 