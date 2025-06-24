from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from datetime import date
#Create your models here.
SELECT_CATEGORY_CHOICES = [
    ("Food","Food"),
    ("Travel","Travel"),
    ("Shopping","Shopping"),
    ("Necessities","Necessities"),
    ("Entertainment","Entertainment"),
    ("Other","Other")
 ]
ADD_EXPENSE_CHOICES = [
     ("Expense","Expense"),
     ("Income","Income")
 ]
PROFESSION_CHOICES =[
    ("Employee","Employee"),
    ("Business","Business"),
    ("Student","Student"),
    ("Other","Other")
]
INVESTMENT_TYPE_CHOICES = [
    ("Stocks", "Stocks"),
    ("Mutual Funds", "Mutual Funds"),
    ("Fixed Deposits", "Fixed Deposits"),
    ("Bonds", "Bonds"),
    ("Real Estate", "Real Estate"),
    ("Gold", "Gold"),
    ("Cryptocurrency", "Cryptocurrency"),
    ("Other", "Other")
]

INVESTMENT_STATUS_CHOICES = [
    ("Active", "Active"),
    ("Sold", "Sold"),
    ("Matured", "Matured"),
    ("Pending", "Pending")
]

RISK_LEVEL_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High")
]

class Addmoney_info(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    add_money = models.CharField(max_length = 10 , choices = ADD_EXPENSE_CHOICES )
    quantity = models.BigIntegerField()
    Date = models.DateField(default = now)
    Category = models.CharField( max_length = 20, choices = SELECT_CATEGORY_CHOICES , default ='Food')
    investment = models.ForeignKey('Investment', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        db_table:'addmoney'
        
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profession = models.CharField(max_length = 10, choices=PROFESSION_CHOICES)
    Savings = models.IntegerField( null=True, blank=True)
    income = models.BigIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_image',blank=True)
    def __str__(self):
       return self.user.username
   
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link budget to a user
    name = models.CharField(max_length=100) # e.g., "Groceries Budget"
    amount = models.DecimalField(max_digits=10, decimal_places=2) # The budget amount
    category = models.CharField(max_length=50) # The category the budget is for
    period = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')]) # How often the budget resets
    created_at = models.DateTimeField(auto_now_add=True) # When the budget was created

    def __str__(self):
        return f"{self.name} for {self.user.username} ({self.period})"

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=10, blank=True, null=True, help_text="Stock symbol for real-time tracking (e.g., AAPL)")
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField()
    maturity_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=INVESTMENT_STATUS_CHOICES, default="Active")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default="Medium")
    target_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_price_update = models.DateTimeField(null=True, blank=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.investment_type}"

    @property
    def returns(self):
        return self.current_value - self.amount_invested

    @property
    def returns_percentage(self):
        if self.amount_invested == 0:
            return 0
        return ((self.current_value - self.amount_invested) / self.amount_invested) * 100

    @property
    def holding_period(self):
        """Calculate the holding period in days"""
        return (date.today() - self.purchase_date).days

    @property
    def days_to_maturity(self):
        """Calculate days remaining until maturity"""
        if self.maturity_date:
            return (self.maturity_date - date.today()).days
        return None

    @property
    def annualized_return(self):
        """Calculate annualized return rate"""
        if self.holding_period > 0:
            years = float(self.holding_period) / 365.0
            if years > 0:
                base = 1 + float(self.returns_percentage) / 100
                return (base ** (1 / years) - 1) * 100
        return 0

    @property
    def risk_score(self):
        """Calculate a risk score based on investment type, volatility, and market conditions"""
        base_risk_scores = {
            'Stocks': 8,
            'Mutual Funds': 6,
            'Fixed Deposits': 2,
            'Bonds': 3,
            'Real Estate': 5,
            'Gold': 4,
            'Cryptocurrency': 9,
            'Other': 5
        }
        
        risk_score = base_risk_scores.get(self.investment_type, 5)
        
        # Adjust risk based on stop loss and target price
        if self.stop_loss and self.target_price:
            risk_range = abs(self.target_price - self.stop_loss) / self.current_value * 100
            risk_score += min(risk_range / 10, 2)  # Max 2 points from risk range
            
        # Adjust risk based on holding period
        if self.holding_period < 30:  # Less than a month
            risk_score += 1
        elif self.holding_period > 365:  # More than a year
            risk_score -= 1
            
        return min(max(risk_score, 1), 10)  # Ensure score is between 1 and 10

    @property
    def portfolio_weight(self):
        """Calculate this investment's weight in the total portfolio"""
        try:
            total_portfolio = Investment.objects.filter(
                user=self.user, 
                status='Active'
            ).aggregate(total=models.Sum('current_value'))['total'] or 0
            if total_portfolio > 0:
                return (self.current_value / total_portfolio) * 100
        except:
            pass
        return 0

    def update_real_time_price(self):
        """Update current value from real-time market data"""
        from .utils import get_real_time_stock_price
        if self.stock_symbol:
            price_data = get_real_time_stock_price(self.stock_symbol)
            if price_data and price_data['current_price']:
                self.current_value = price_data['current_price'] * self.quantity
                self.last_price_update = now()
                self.pe_ratio = price_data['pe_ratio']
                self.dividend_yield = price_data['dividend_yield']
                self.save()
                return True
        return False

    class Meta:
        ordering = ['-purchase_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['investment_type']),
            models.Index(fields=['purchase_date']),
            models.Index(fields=['stock_symbol']),
        ]

class InvestmentValueHistory(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='value_history')
    date = models.DateField()
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.investment.name} on {self.date}: {self.value}"

