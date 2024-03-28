from django.shortcuts import render, redirect
from .models import Stock  # Assuming Stock model is defined in models.py
import yfinance as yf
def add_stock(request):
    if request.method == 'POST':
        # Process form submission
        ticker = request.POST.get('ticker')
        quantity = int(request.POST.get('quantity'))
        
        # Save the stock to the database
        stock_data = yf.Ticker(ticker).history(period="1d")
        price = stock_data['Close'].iloc[-1]
        value = price * quantity
        Stock.objects.create(ticker=ticker, quantity=quantity, price=price, value=value)
        
        return redirect('portfolio')  # Redirect to portfolio page after adding the stock
    else:
        return render(request, 'add_stock.html')