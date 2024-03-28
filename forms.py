from django import forms

class StockForm(forms.Form):
    ticker = forms.CharField(label='Ticker', max_length=10)
    quantity = forms.IntegerField(label='Quantity')