import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import yfinance as yf

class StockPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio")
        
        # Initialize DataFrame to store portfolio data
        self.portfolio_df = pd.DataFrame(columns=['Ticker', 'Quantity', 'Price', 'Value'])
        
        # Load existing portfolio data from CSV if available
        try:
            self.portfolio_df = pd.read_csv('portfolio.csv')
        except FileNotFoundError:
            pass
        
        # Create Treeview for displaying portfolio
        self.tree = ttk.Treeview(self.root, columns=['Quantity', 'Price', 'Value'], show='headings')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Value', text='Value')
        self.tree.pack(padx=10, pady=10)
        
        # Populate Treeview with existing portfolio data
        self.update_portfolio_view()
        
        # Add ticker and quantity fields
        ttk.Label(self.root, text="Ticker:").pack()
        self.ticker_entry = ttk.Entry(self.root)
        self.ticker_entry.pack()
        
        ttk.Label(self.root, text="Quantity:").pack()
        self.quantity_entry = ttk.Entry(self.root)
        self.quantity_entry.pack()
        
        # Add buttons for adding and deleting entries
        ttk.Button(self.root, text="Add", command=self.add_stock).pack(pady=5)
        ttk.Button(self.root, text="Delete", command=self.delete_stock).pack()
        
    def add_stock(self):
        ticker = self.ticker_entry.get().upper()
        quantity = int(self.quantity_entry.get())
        
        try:
            stock_data = yf.Ticker(ticker).history(period="1d")
            price = stock_data['Close'].iloc[-1]
            value = price * quantity
            self.portfolio_df = self.portfolio_df.append({'Ticker': ticker, 'Quantity': quantity, 'Price': price, 'Value': value}, ignore_index=True)
            self.portfolio_df.to_csv('portfolio.csv', index=False)  # Save portfolio to CSV
            self.update_portfolio_view()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def delete_stock(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return
        
        ticker_to_delete = self.tree.item(selected_item, 'values')[0]
        self.portfolio_df = self.portfolio_df[self.portfolio_df['Ticker'] != ticker_to_delete]
        self.portfolio_df.to_csv('portfolio.csv', index=False)  # Save portfolio to CSV
        self.update_portfolio_view()
        
    def update_portfolio_view(self):
        # Clear existing data in Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert portfolio data into Treeview
        for index, row in self.portfolio_df.iterrows():
            self.tree.insert('', 'end', values=(row['Ticker'], row['Quantity'], row['Price'], row['Value']))

def main():
    root = tk.Tk()
    app = StockPortfolioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()