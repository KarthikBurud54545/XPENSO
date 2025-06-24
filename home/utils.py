import requests
from decimal import Decimal
from django.conf import settings
import json

def get_real_time_stock_price(symbol):
    """
    Get real-time stock price using Alpha Vantage API
    """
    try:
        url = f'https://www.alphavantage.co/query'
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': settings.ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json().get('Global Quote', {})
        
        return {
            'current_price': Decimal(str(data.get('05. price', 0))),
            'change': Decimal(str(data.get('09. change', 0))),
            'change_percent': Decimal(str(data.get('10. change percent', '0').strip('%'))),
            'volume': int(data.get('06. volume', 0)),
            'market_cap': 0,  # Not available in basic quote endpoint
            'pe_ratio': None,  # Will be fetched separately if needed
            'dividend_yield': None,  # Will be fetched separately if needed
            'company_name': '',  # Will be fetched separately if needed
            'currency': 'USD'
        }
    except Exception as e:
        return None

def get_stock_historical_data(symbol, period='1y'):
    """
    Get historical stock data using Alpha Vantage API
    """
    try:
        url = f'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'apikey': settings.ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json().get('Time Series (Daily)', {})
        
        # Convert to list of dictionaries
        records = []
        for date, values in data.items():
            records.append({
                'Date': date,
                'Open': float(values['1. open']),
                'High': float(values['2. high']),
                'Low': float(values['3. low']),
                'Close': float(values['4. close']),
                'Volume': float(values['5. volume'])
            })
        
        # Sort by date in descending order
        records.sort(key=lambda x: x['Date'], reverse=True)
        
        # Limit to last year if period is '1y'
        if period == '1y':
            records = records[:252]  # Approximately 252 trading days in a year
            
        return records
    except Exception as e:
        return []

def get_market_news():
    """
    Get latest market news using NewsAPI
    """
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'stock market OR finance OR investing',
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 10,
            'apiKey': settings.NEWS_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('articles', [])
        return []
    except Exception as e:
        return []

def calculate_portfolio_metrics(investments):
    """
    Calculate advanced portfolio metrics
    """
    total_value = sum(inv.current_value for inv in investments)
    metrics = {
        'total_value': total_value,
        'asset_allocation': {},
        'risk_metrics': {
            'sharpe_ratio': 0,
            'beta': 0,
            'alpha': 0,
            'r_squared': 0
        },
        'performance_metrics': {
            'ytd_return': 0,
            'one_year_return': 0,
            'three_year_return': 0,
            'five_year_return': 0
        }
    }
    
    # Calculate asset allocation
    for inv in investments:
        asset_type = inv.investment_type
        if asset_type not in metrics['asset_allocation']:
            metrics['asset_allocation'][asset_type] = 0
        metrics['asset_allocation'][asset_type] += (inv.current_value / total_value) * 100
    
    return metrics

def get_portfolio_recommendations(investments):
    """
    Generate portfolio rebalancing recommendations
    """
    recommendations = []
    total_value = sum(inv.current_value for inv in investments)
    
    # Ideal asset allocation targets
    ideal_allocation = {
        'Stocks': 60,
        'Bonds': 20,
        'Real Estate': 10,
        'Gold': 5,
        'Cryptocurrency': 5
    }
    
    # Calculate current allocation
    current_allocation = {}
    for inv in investments:
        asset_type = inv.investment_type
        if asset_type not in current_allocation:
            current_allocation[asset_type] = 0
        current_allocation[asset_type] += (inv.current_value / total_value) * 100
    
    # Generate recommendations
    for asset_type, ideal_percent in ideal_allocation.items():
        current_percent = current_allocation.get(asset_type, 0)
        diff = ideal_percent - current_percent
        
        if abs(diff) >= 5:  # Only recommend changes for differences >= 5%
            action = 'increase' if diff > 0 else 'decrease'
            recommendations.append({
                'asset_type': asset_type,
                'action': action,
                'current_allocation': current_percent,
                'target_allocation': ideal_percent,
                'difference': abs(diff)
            })
    
    return sorted(recommendations, key=lambda x: abs(x['difference']), reverse=True) 