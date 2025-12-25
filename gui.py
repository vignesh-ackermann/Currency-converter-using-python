import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/convert"


def convert_currency():
    from_cur = from_entry.get().strip().upper()
    to_cur = to_entry.get().strip().upper()
    amount = amount_entry.get().strip()

    if not from_cur or not to_cur or not amount:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be numeric")
        return

    params = {
        "from_currency": from_cur,
        "to_currency": to_cur,
        "amount": amount
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data.get("detail"))
            return

        result_label.config(
            text=f"Rate: {data['rate']}\nConverted Amount: {data['converted_amount']}"
        )

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Backend not running")


# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("API-Based Currency Converter")
root.geometry("360x320")
root.resizable(False, False)

tk.Label(root, text="API-Based Currency Converter",
         font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="From Currency (USD, EUR, INR)").pack()
from_entry = tk.Entry(root)
from_entry.pack(pady=5)

tk.Label(root, text="To Currency (INR, USD, EUR)").pack()
to_entry = tk.Entry(root)
to_entry.pack(pady=5)

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

tk.Button(root, text="Convert",
          width=15, bg="green", fg="white",
          command=convert_currency).pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
result_label.pack(pady=10)

root.mainloop()
