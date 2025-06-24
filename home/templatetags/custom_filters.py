from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def div(value, arg):
    """
    Divides the value by the argument
    """
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """Multiplies the arg and the value"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def percentage(value, total):
    try:
        value = float(value)
        total = float(total)
        if total > 0:
            return round((value / total) * 100, 1)
        return 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def percentage_change(current, previous):
    """
    Calculate the percentage change between current and previous values.
    Example: if previous is 100 and current is 150, return 50 (% increase)
    """
    try:
        current = Decimal(str(current))
        previous = Decimal(str(previous))
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / abs(previous)) * 100, 1)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter
def trend(current, previous):
    try:
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((Decimal(str(current)) - Decimal(str(previous))) / Decimal(str(abs(previous)))) * 100, 1)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter(name='abs_value')
def abs_value(value):
    """Return the absolute value of a number."""
    try:
        return abs(value)
    except (TypeError, ValueError):
        return value

@register.filter
def subtract(value, arg):
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divisibleby(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def get_item(dictionary, key):
    """
    Custom template filter to get a value from a dictionary using a key.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key, None)

@register.filter
def currency(value):
    """
    Format a number as currency with ₹ symbol and 2 decimal places.
    Usage: {{ value|currency }}
    """
    try:
        decimal_value = Decimal(str(value))
        return f"₹{decimal_value:,.2f}"
    except (ValueError, TypeError, decimal.InvalidOperation):
        return "₹0.00"

@register.filter(name='investment_icon')
def investment_icon(investment_type):
    """Returns a Font Awesome icon class based on the investment type."""
    icon_map = {
        'stocks': 'fas fa-chart-line',
        'mutual_funds': 'fas fa-users',
        'bonds': 'fas fa-file-contract',
        'real_estate': 'fas fa-building',
        'crypto': 'fab fa-bitcoin',
        'fd': 'fas fa-piggy-bank',
        'gold': 'fas fa-gem',
        'other': 'fas fa-briefcase',
    }
    key = str(investment_type).strip().lower().replace(" ", "_")
    return icon_map.get(key, 'fas fa-briefcase')

@register.filter(name='investment_color')
def investment_color(investment_type):
    """Returns a color based on the investment type."""
    color_map = {
        'stocks': '#4A90E2',
        'mutual_funds': '#50E3C2',
        'bonds': '#B8E986',
        'real_estate': '#F8E71C',
        'crypto': '#F5A623',
        'fd': '#9013FE',
        'gold': '#D0A03E',
        'other': '#787878',
    }
    key = str(investment_type).strip().lower().replace(" ", "_")
    return color_map.get(key, '#787878')

@register.filter(name='status_color_bg')
def status_color_bg(status):
    return '#2E7D32' if status == 'Active' else '#C62828'

@register.filter(name='status_color_text')
def status_color_text(status):
    return '#FFFFFF' 