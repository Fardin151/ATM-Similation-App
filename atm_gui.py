import tkinter as tk
from tkinter import messagebox


# ---------------- ATM LOGIC ----------------
class ATM:
    def __init__(self, pin="1234", balance=0):
        self.pin = pin
        self.balance = balance

    def check_pin(self, entered_pin):
        return entered_pin == self.pin

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Successfully deposited ${amount:.2f}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid withdrawal amount"
        if amount > self.balance:
            return "Insufficient balance"
        self.balance -= amount
        return f"Successfully withdrew ${amount:.2f}"


# ---------------- GUI APP ----------------
atm = ATM()

root = tk.Tk()
root.title("ATM Simulation")
root.geometry("320x320")
root.resizable(False, False)


# ---------------- LOGIN SCREEN ----------------
def login():
    entered_pin = pin_entry.get()
    if atm.check_pin(entered_pin):
        login_frame.pack_forget()
        atm_frame.pack()
    else:
        messagebox.showerror("Error", "Incorrect PIN")


login_frame = tk.Frame(root)
login_frame.pack(pady=60)

tk.Label(login_frame, text="ATM Login", font=("Arial", 16)).pack(pady=10)
tk.Label(login_frame, text="Enter PIN").pack()

pin_entry = tk.Entry(login_frame, show="*", width=20)
pin_entry.pack(pady=5)

tk.Button(login_frame, text="Login", width=15, command=login).pack(pady=10)


# ---------------- ATM DASHBOARD ----------------
def check_balance():
    messagebox.showinfo("Balance", f"Your balance is ${atm.balance:.2f}")

def deposit():
    try:
        amount = float(amount_entry.get())
        messagebox.showinfo("Deposit", atm.deposit(amount))
        amount_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")

def withdraw():
    try:
        amount = float(amount_entry.get())
        messagebox.showinfo("Withdraw", atm.withdraw(amount))
        amount_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")

def exit_app():
    root.destroy()


atm_frame = tk.Frame(root)

tk.Label(atm_frame, text="ATM Menu", font=("Arial", 16)).pack(pady=10)

amount_entry = tk.Entry(atm_frame, width=25)
amount_entry.pack(pady=5)
amount_entry.insert(0, "Enter amount")

tk.Button(atm_frame, text="Check Balance", width=25, command=check_balance).pack(pady=4)
tk.Button(atm_frame, text="Deposit", width=25, command=deposit).pack(pady=4)
tk.Button(atm_frame, text="Withdraw", width=25, command=withdraw).pack(pady=4)
tk.Button(atm_frame, text="Exit", width=25, command=exit_app).pack(pady=10)


# ---------------- START APP ----------------
root.mainloop()