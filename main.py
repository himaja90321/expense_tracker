import tkinter as tk
from tkinter import messagebox
import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt

# File to store expenses
FILENAME = 'expenses.csv'

# Create CSV file with headers if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Category', 'Amount'])

# Add new expense
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount])

    messagebox.showinfo("Success", "Expense added!")
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Show pie chart of expenses by category
def show_chart():
    data = defaultdict(float)

    with open(FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data[row['Category']] += float(row['Amount'])
            except ValueError:
                continue

    if not data:
        messagebox.showinfo("No Data", "No expenses to show.")
        return

    categories = list(data.keys())
    amounts = list(data.values())
    total = sum(amounts)
    percentages = [f'{(a / total) * 100:.1f}%' for a in amounts]

    # Labels with percentages
    labels = [f'{cat} ({perc})' for cat, perc in zip(categories, percentages)]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=labels, autopct='', startangle=90)
    plt.title("Your Expenses by Category")
    plt.axis('equal')  # Equal aspect ratio ensures pie is round.
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Amount (₹):").grid(row=2, column=0, padx=10, pady=5)

date_entry = tk.Entry(root)
category_entry = tk.Entry(root)
amount_entry = tk.Entry(root)

date_entry.grid(row=0, column=1, padx=10, pady=5)
category_entry.grid(row=1, column=1, padx=10, pady=5)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Show Pie Chart", command=show_chart, bg="#2196F3", fg="white").grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
