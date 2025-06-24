from django import forms
from .models import Addmoney_info, Investment

class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = Addmoney_info
        fields = ['add_money', 'quantity', 'Date', 'Category', 'investment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['investment'].queryset = Investment.objects.filter(user=user)
        else:
            self.fields['investment'].queryset = Investment.objects.none() 