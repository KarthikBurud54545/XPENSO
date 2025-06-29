from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('handleSignup/',views.handleSignup,name='handleSignup'),
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('handleLogout/',views.handleLogout,name='handleLogout'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "home/reset_password.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="home/reset_password_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name ="home/password_reset_form.html"),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetView.as_view(template_name ="home/password_reset_done.html"),name='password_reset_complete'),
    path('addmoney/',views.addmoney,name='addmoney'),
    path('addmoney_submission/',views.addmoney_submission,name='addmoney_submission'),
    path('charts/',views.charts,name='charts'),
    path('tables/',views.tables,name='tables'),
    path('expense_edit/<int:id>/',views.expense_edit,name='expense_edit'),
    path('<int:id>/addmoney_update/', views.addmoney_update, name="addmoney_update") ,
    path('expense_delete/<int:id>/',views.expense_delete,name='expense_delete'),
    path('profile/',views.profile,name = 'profile'),
    path('expense_month/',views.expense_month, name = 'expense_month'),
    path('expense_month_data/',views.expense_month_data, name = 'expense_month_data'),
    path('export/csv/', views.export_transactions_csv, name='export_csv'),
    path('export/excel/', views.export_transactions_excel, name='export_excel'),
    path('export/pdf/', views.export_transactions_pdf, name='export_pdf'),
    path('stats/',views.stats, name = 'stats'),
    path('expense_week/',views.expense_week, name = 'expense_week'),
    path('weekly/',views.weekly, name = 'weekly'),
    path('check/',views.check,name="check"),
    path('search/',views.search,name="search"),
    path('<int:id>/profile_edit/',views.profile_edit,name="profile_edit"),
    path('<int:id>/profile_update/',views.profile_update,name="profile_update"),
    path('info/',views.info,name="info"),
    path('info_year/',views.info_year,name="info_year"),
    path('login/', views.login_page, name='login'),
    path('budgets/', views.budgets_view, name='budgets'),
    path('investments/', views.investments, name='investments'),
    path('add_investment/', views.add_investment, name='add_investment'),
    path('update_investment/<int:id>/', views.update_investment, name='update_investment'),
    path('delete_investment/<int:id>/', views.delete_investment, name='delete_investment'),
    path('investment/<int:id>/', views.view_investment, name='view_investment'),
    path('investment_dashboard/', views.investment_dashboard_full, name='investment_dashboard_full'),
    path('investment_dashboard/<int:id>/', views.investment_dashboard, name='investment_dashboard'),
    path('monthly_trend/', views.monthly_trend, name='monthly_trend'),
    path('forecast/', views.spending_forecast, name='forecast'),
    path('api/market-data/', views.get_market_data, name='market_data'),
    path('api/market-news/', views.get_market_news_api, name='market_news'),
    
    # Transaction management endpoints
    path('api/transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('api/transaction/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transaction/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('api/investments/realtime/', views.api_investment_realtime, name='api_investment_realtime'),
    path('export/investments/csv/', views.export_investments_csv, name='export_investments_csv'),
    path('export/investments/excel/', views.export_investments_excel, name='export_investments_excel'),
    path('export/investments/pdf/', views.export_investments_pdf, name='export_investments_pdf'),
    path('analytics/', views.investment_dashboard, {'id': 0}, name='analytics_dashboard'),
    path('budgets/edit/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('budgets/delete/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    path('export/investment/<int:id>/csv/', views.export_investment_csv, name='export_investment_csv'),
]
