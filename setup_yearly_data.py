import os
import django
import datetime
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpenseTracker.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import Addmoney_info

def setup_yearly_data():
    try:
        # Get the first user (assuming this is your user)
        user = User.objects.first()
        if not user:
            print("No users found in the database. Please create a user first.")
            return

        # Sample expense categories with typical monthly ranges
        categories = {
            'Food & Groceries': (3000, 5000),  # Essential, relatively stable
            'Rent': (10000, 10000),  # Fixed cost
            'Transportation': (1500, 2500),  # Variable but moderate
            'Shopping': (2000, 4000),  # More variable
            'Entertainment': (1000, 3000),  # Discretionary
            'Utilities': (2000, 3000),  # Somewhat stable
            'Healthcare': (500, 2000),  # Occasional
            'Education': (1000, 3000),  # Periodic
        }

        # Current year and previous year
        current_year = datetime.datetime.now().year
        previous_year = current_year - 1

        # Create expenses for both years
        for year in [previous_year, current_year]:
            print(f"\nCreating expenses for year {year}:")
            
            for month in range(1, 13):
                # Skip future months in current year
                if year == current_year and month > datetime.datetime.now().month:
                    continue

                # Date for this month's expenses
                date = datetime.date(year, month, random.randint(1, 28))

                # Create expenses for each category
                for category, (min_amount, max_amount) in categories.items():
                    # Add some randomness to amounts while maintaining patterns
                    if category == 'Rent':
                        amount = max_amount  # Rent stays constant
                    else:
                        # Add seasonal variations
                        season_factor = 1.0
                        if category == 'Entertainment':
                            # More entertainment in summer months
                            if month in [6, 7, 8]:
                                season_factor = 1.3
                        elif category == 'Shopping':
                            # More shopping in festival/holiday months
                            if month in [11, 12]:
                                season_factor = 1.5
                        elif category == 'Utilities':
                            # Higher in winter and summer
                            if month in [1, 2, 6, 7, 8]:
                                season_factor = 1.2

                        base_amount = random.uniform(min_amount, max_amount)
                        amount = round(base_amount * season_factor)

                    # Create the expense record
                    Addmoney_info.objects.create(
                        user=user,
                        Category=category,
                        Date=date,
                        add_money='Expense',
                        quantity=amount
                    )
                    print(f"Added {category} expense for {date.strftime('%B %Y')}: ₹{amount}")

                # Add some income entries (salary and occasional bonus)
                base_salary = 50000
                if month == 12:  # Year-end bonus
                    bonus = base_salary * 0.5
                else:
                    bonus = 0

                Addmoney_info.objects.create(
                    user=user,
                    Category='Salary',
                    Date=date,
                    add_money='Income',
                    quantity=base_salary + bonus
                )
                print(f"Added Salary for {date.strftime('%B %Y')}: ₹{base_salary + bonus}")

        print("\nSample yearly data setup completed successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    # Clear existing data first
    user = User.objects.first()
    if user:
        print("Clearing existing transaction data...")
        Addmoney_info.objects.filter(user=user).delete()
    
    setup_yearly_data() 