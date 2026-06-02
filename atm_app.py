"""
Enhanced ATM Simulation
Features:
  - Modern dark UI design
  - Transaction history window
  - Multiple user accounts
  - Save/load data to JSON file
  - Packagable as .exe via PyInstaller
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ─────────────────────────────────────────
#  CONSTANTS & THEME
# ─────────────────────────────────────────
DATA_FILE = "atm_data.json"

COLORS = {
    "bg":        "#0D0D0F",
    "surface":   "#16161A",
    "card":      "#1E1E24",
    "border":    "#2A2A32",
    "accent":    "#00D4AA",
    "accent2":   "#7C3AED",
    "danger":    "#FF4757",
    "warning":   "#FFD32A",
    "text":      "#F0F0F5",
    "subtext":   "#888899",
    "input_bg":  "#252530",
}

FONTS = {
    "display":  ("Consolas", 30, "bold"),
    "heading":  ("Consolas", 18, "bold"),
    "body":     ("Consolas", 14),
    "small":    ("Consolas", 12),
    "mono":     ("Courier New", 14),
}

# ─────────────────────────────────────────
#  DATA LAYER  (accounts saved to JSON)
# ─────────────────────────────────────────
DEFAULT_ACCOUNTS = {
    "1001": {"pin": "1234", "name": "Alice Johnson",   "balance": 5000.00, "transactions": []},
    "1002": {"pin": "4321", "name": "Bob Smith",       "balance": 2500.00, "transactions": []},
    "1003": {"pin": "0000", "name": "Charlie Brown",   "balance": 750.00,  "transactions": []},
}


def load_accounts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_ACCOUNTS.copy()


def save_accounts(accounts):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(accounts, f, indent=2)
    except IOError as e:
        messagebox.showerror("Save Error", f"Could not save data:\n{e}")


# ─────────────────────────────────────────
#  ATM LOGIC
# ─────────────────────────────────────────
class ATM:
    def __init__(self):
        self.accounts = load_accounts()
        self.current_id = None

    # ── auth ──────────────────────────────
    def login(self, account_id, pin):
        acc = self.accounts.get(account_id)
        if acc and acc["pin"] == pin:
            self.current_id = account_id
            return True
        return False

    def logout(self):
        self.current_id = None

    # ── helpers ───────────────────────────
    @property
    def account(self):
        return self.accounts[self.current_id]

    @property
    def balance(self):
        return self.account["balance"]

    def _record(self, kind, amount, note=""):
        entry = {
            "type":   kind,
            "amount": amount,
            "note":   note,
            "time":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": self.account["balance"],
        }
        self.account["transactions"].append(entry)
        save_accounts(self.accounts)

    # ── operations ────────────────────────
    def deposit(self, amount):
        if amount <= 0:
            return False, "Amount must be greater than zero."
        self.account["balance"] += amount
        self._record("DEPOSIT", amount)
        return True, f"Deposited ${amount:,.2f} successfully."

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Amount must be greater than zero."
        if amount > self.balance:
            return False, f"Insufficient funds. Available: ${self.balance:,.2f}"
        self.account["balance"] -= amount
        self._record("WITHDRAWAL", amount)
        return True, f"Withdrew ${amount:,.2f} successfully."

    def transfer(self, target_id, amount):
        if target_id == self.current_id:
            return False, "Cannot transfer to yourself."
        if target_id not in self.accounts:
            return False, f"Account {target_id} not found."
        if amount <= 0:
            return False, "Amount must be greater than zero."
        if amount > self.balance:
            return False, f"Insufficient funds. Available: ${self.balance:,.2f}"
        self.account["balance"] -= amount
        self._record("TRANSFER OUT", amount, f"To {target_id}")
        self.accounts[target_id]["balance"] += amount
        self.accounts[target_id]["transactions"].append({
            "type":   "TRANSFER IN",
            "amount": amount,
            "note":   f"From {self.current_id}",
            "time":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": self.accounts[target_id]["balance"],
        })
        save_accounts(self.accounts)
        return True, f"Transferred ${amount:,.2f} to account {target_id}."

    def change_pin(self, old_pin, new_pin):
        if old_pin != self.account["pin"]:
            return False, "Current PIN is incorrect."
        if len(new_pin) != 4 or not new_pin.isdigit():
            return False, "New PIN must be exactly 4 digits."
        self.account["pin"] = new_pin
        save_accounts(self.accounts)
        return True, "PIN changed successfully."


# ─────────────────────────────────────────
#  REUSABLE UI HELPERS
# ─────────────────────────────────────────
def styled_frame(parent, **kw):
    return tk.Frame(parent, bg=COLORS["bg"], **kw)


def card_frame(parent, **kw):
    return tk.Frame(parent, bg=COLORS["card"],
                    highlightbackground=COLORS["border"],
                    highlightthickness=1, **kw)


def label(parent, text, style="body", fg=None, **kw):
    fg = fg or COLORS["text"]
    return tk.Label(parent, text=text, font=FONTS[style],
                    bg=parent["bg"], fg=fg, **kw)


def entry_field(parent, show=None, width=22):
    e = tk.Entry(parent, show=show, width=width,
                 font=FONTS["body"],
                 bg=COLORS["input_bg"], fg=COLORS["text"],
                 insertbackground=COLORS["accent"],
                 relief="flat",
                 highlightbackground=COLORS["border"],
                 highlightthickness=1,
                 highlightcolor=COLORS["accent"])
    return e


def accent_button(parent, text, command, color=None, width=22):
    color = color or COLORS["accent"]
    btn = tk.Button(parent, text=text, command=command,
                    width=width, font=FONTS["body"],
                    bg=color, fg=COLORS["bg"],
                    activebackground=COLORS["bg"],
                    activeforeground=color,
                    relief="flat", cursor="hand2", pady=6)
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["bg"], fg=color,
                                             highlightbackground=color,
                                             highlightthickness=1))
    btn.bind("<Leave>", lambda e: btn.config(bg=color, fg=COLORS["bg"],
                                             highlightthickness=0))
    return btn


def ghost_button(parent, text, command, width=22):
    btn = tk.Button(parent, text=text, command=command,
                    width=width, font=FONTS["body"],
                    bg=COLORS["card"], fg=COLORS["subtext"],
                    activebackground=COLORS["border"],
                    activeforeground=COLORS["text"],
                    relief="flat", cursor="hand2", pady=6,
                    highlightbackground=COLORS["border"],
                    highlightthickness=1)
    return btn


# ─────────────────────────────────────────
#  TRANSACTION HISTORY WINDOW
# ─────────────────────────────────────────
def open_history(atm_obj, parent):
    win = tk.Toplevel(parent)
    win.title("Transaction History")
    win.geometry("720x520")
    win.configure(bg=COLORS["bg"])
    win.resizable(False, False)

    # Header
    hdr = tk.Frame(win, bg=COLORS["card"], pady=12)
    hdr.pack(fill="x")
    label(hdr, f"  Transaction History — {atm_obj.account['name']}",
          "heading").pack(side="left", padx=16)

    txns = list(reversed(atm_obj.account["transactions"]))

    if not txns:
        label(win, "No transactions yet.", fg=COLORS["subtext"]).pack(pady=40)
        return

    # Scrollable list
    container = tk.Frame(win, bg=COLORS["bg"])
    container.pack(fill="both", expand=True, padx=16, pady=12)

    canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical",
                               command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=COLORS["bg"])

    scroll_frame.bind("<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Columns header
    cols = tk.Frame(scroll_frame, bg=COLORS["surface"], pady=6)
    cols.pack(fill="x", pady=(0, 4))
    for txt, w in [("DATE & TIME", 22), ("TYPE", 16), ("AMOUNT", 14), ("BALANCE", 14)]:
        tk.Label(cols, text=txt, font=FONTS["small"],
                 bg=COLORS["surface"], fg=COLORS["subtext"],
                 width=w, anchor="w").pack(side="left", padx=4)

    type_colors = {
        "DEPOSIT":      COLORS["accent"],
        "WITHDRAWAL":   COLORS["danger"],
        "TRANSFER OUT": COLORS["warning"],
        "TRANSFER IN":  COLORS["accent"],
    }

    for i, t in enumerate(txns):
        row_bg = COLORS["card"] if i % 2 == 0 else COLORS["bg"]
        row = tk.Frame(scroll_frame, bg=row_bg, pady=5)
        row.pack(fill="x")

        tk.Label(row, text=t["time"], font=FONTS["small"],
                 bg=row_bg, fg=COLORS["subtext"], width=20, anchor="w"
                 ).pack(side="left", padx=4)

        tcolor = type_colors.get(t["type"], COLORS["text"])
        tk.Label(row, text=t["type"], font=FONTS["small"],
                 bg=row_bg, fg=tcolor, width=14, anchor="w"
                 ).pack(side="left", padx=4)

        sign = "+" if "IN" in t["type"] or t["type"] == "DEPOSIT" else "-"
        tk.Label(row, text=f"{sign}${t['amount']:,.2f}", font=FONTS["small"],
                 bg=row_bg, fg=tcolor, width=12, anchor="w"
                 ).pack(side="left", padx=4)

        tk.Label(row, text=f"${t['balance_after']:,.2f}", font=FONTS["small"],
                 bg=row_bg, fg=COLORS["text"], width=12, anchor="w"
                 ).pack(side="left", padx=4)

        if t.get("note"):
            tk.Label(row, text=f"  ↳ {t['note']}", font=FONTS["small"],
                     bg=row_bg, fg=COLORS["subtext"]
                     ).pack(side="left")

    # Mouse wheel scroll
    def _scroll(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    canvas.bind_all("<MouseWheel>", _scroll)


# ─────────────────────────────────────────
#  CHANGE PIN WINDOW
# ─────────────────────────────────────────
def open_change_pin(atm_obj, parent):
    win = tk.Toplevel(parent)
    win.title("Change PIN")
    win.geometry("400x340")
    win.configure(bg=COLORS["bg"])
    win.resizable(False, False)

    tk.Frame(win, bg=COLORS["card"], pady=10).pack(fill="x")
    label(win, "Change PIN", "heading").pack(pady=(20, 4))

    c = card_frame(win, padx=24, pady=20)
    c.pack(padx=24, pady=8, fill="x")

    label(c, "Current PIN").pack(anchor="w")
    old_e = entry_field(c, show="*")
    old_e.pack(pady=(2, 10))

    label(c, "New PIN (4 digits)").pack(anchor="w")
    new_e = entry_field(c, show="*")
    new_e.pack(pady=(2, 10))

    def do_change():
        ok, msg = atm_obj.change_pin(old_e.get(), new_e.get())
        if ok:
            messagebox.showinfo("Success", msg, parent=win)
            win.destroy()
        else:
            messagebox.showerror("Error", msg, parent=win)

    accent_button(c, "CHANGE PIN", do_change).pack(pady=4)


# ─────────────────────────────────────────
#  MAIN APP WINDOW
# ─────────────────────────────────────────
class ATMApp:
    def __init__(self):
        self.atm = ATM()

        self.root = tk.Tk()
        self.root.title("ATM Simulation")
        self.root.geometry("580x760")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 580) // 2
        y = (self.root.winfo_screenheight() - 760) // 2
        self.root.geometry(f"580x760+{x}+{y}")

        self._build_login()
        self.root.mainloop()

    # ── LOGIN SCREEN ──────────────────────
    def _build_login(self):
        self.login_frame = styled_frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        # Top banner
        banner = tk.Frame(self.login_frame, bg=COLORS["card"], height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner, text="◈  ATM", font=("Consolas", 36, "bold"),
                 bg=COLORS["card"], fg=COLORS["accent"]).pack(expand=True)

        # Card
        c = card_frame(self.login_frame, padx=40, pady=36)
        c.pack(padx=50, pady=30, fill="x")

        label(c, "Welcome Back", "heading").pack(anchor="w")
        label(c, "Sign in to your account", fg=COLORS["subtext"]).pack(anchor="w", pady=(2, 24))

        label(c, "Account Number").pack(anchor="w")
        self.id_entry = entry_field(c, width=28)
        self.id_entry.pack(pady=(2, 16), ipady=6)

        label(c, "PIN").pack(anchor="w")
        self.pin_entry = entry_field(c, show="●", width=28)
        self.pin_entry.pack(pady=(2, 24), ipady=6)

        accent_button(c, "SIGN IN", self._do_login, width=28).pack(fill="x")

        # Hint
        hint = card_frame(self.login_frame, padx=20, pady=14)
        hint.pack(padx=50, fill="x")
        label(hint, "Demo accounts:", "small", fg=COLORS["subtext"]).pack(anchor="w")
        for aid, data in self.atm.accounts.items():
            label(hint, f"  {aid}  PIN: {data['pin']}  — {data['name']}",
                  "small", fg=COLORS["subtext"]).pack(anchor="w")

        self.pin_entry.bind("<Return>", lambda e: self._do_login())

    def _do_login(self):
        aid  = self.id_entry.get().strip()
        pin  = self.pin_entry.get().strip()
        if self.atm.login(aid, pin):
            self.login_frame.destroy()
            self._build_dashboard()
        else:
            messagebox.showerror("Login Failed",
                                 "Invalid account number or PIN.",
                                 parent=self.root)
            self.pin_entry.delete(0, tk.END)

    # ── DASHBOARD ─────────────────────────
    def _build_dashboard(self):
        self.dash_frame = styled_frame(self.root)
        self.dash_frame.pack(fill="both", expand=True)

        # Top bar
        top = tk.Frame(self.dash_frame, bg=COLORS["card"], pady=12, padx=20)
        top.pack(fill="x")
        tk.Label(top, text="◈  ATM", font=FONTS["heading"],
                 bg=COLORS["card"], fg=COLORS["accent"]).pack(side="left")
        tk.Label(top, text=self.atm.account["name"],
                 font=FONTS["small"],
                 bg=COLORS["card"], fg=COLORS["subtext"]).pack(side="right")

        # Balance card
        self.bal_var = tk.StringVar()
        self._refresh_balance()

        bal_card = tk.Frame(self.dash_frame, bg=COLORS["accent2"],
                            padx=30, pady=24)
        bal_card.pack(padx=30, pady=(24, 10), fill="x")
        label(bal_card, "Available Balance", "body",
              fg="#c4b5fd").pack(anchor="w")
        tk.Label(bal_card, textvariable=self.bal_var,
                 font=("Consolas", 38, "bold"),
                 bg=COLORS["accent2"], fg=COLORS["text"]).pack(anchor="w", pady=(6, 0))
        label(bal_card, f"Account  {self.atm.current_id}", "small",
              fg="#c4b5fd").pack(anchor="w", pady=(6, 0))

        # Amount entry
        amt_row = styled_frame(self.dash_frame)
        amt_row.pack(padx=30, pady=(18, 0), fill="x")
        label(amt_row, "Amount  $").pack(side="left")
        self.amt_entry = entry_field(amt_row, width=22)
        self.amt_entry.pack(side="left", padx=10, ipady=6)

        # Action buttons grid
        btn_frame = styled_frame(self.dash_frame)
        btn_frame.pack(padx=30, pady=14, fill="x")

        left  = styled_frame(btn_frame)
        right = styled_frame(btn_frame)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))

        accent_button(left,  "DEPOSIT",  self._do_deposit,  color=COLORS["accent"],  width=18).pack(fill="x", pady=5)
        accent_button(right, "WITHDRAW", self._do_withdraw, color=COLORS["danger"],  width=18).pack(fill="x", pady=5)
        accent_button(left,  "TRANSFER", self._open_transfer, color=COLORS["accent2"], width=18).pack(fill="x", pady=5)
        ghost_button( right, "HISTORY",  lambda: open_history(self.atm, self.root), width=18).pack(fill="x", pady=5)

        # Secondary actions
        sec = styled_frame(self.dash_frame)
        sec.pack(padx=30, fill="x")
        ghost_button(sec, "CHANGE PIN",
                     lambda: open_change_pin(self.atm, self.root),
                     width=18).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ghost_button(sec, "SIGN OUT",
                     self._logout, width=18).pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.dash_frame, textvariable=self.status_var,
                 font=FONTS["small"], bg=COLORS["surface"],
                 fg=COLORS["subtext"], pady=6).pack(side="bottom", fill="x")

    def _refresh_balance(self):
        self.bal_var.set(f"${self.atm.balance:,.2f}")

    def _get_amount(self):
        raw = self.amt_entry.get().strip().replace(",", "")
        try:
            v = float(raw)
            return v, None
        except ValueError:
            return None, "Please enter a valid number."

    def _set_status(self, msg, ok=True):
        self.status_var.set(msg)
        self.root.after(4000, lambda: self.status_var.set("Ready"))

    def _do_deposit(self):
        amount, err = self._get_amount()
        if err:
            messagebox.showerror("Error", err, parent=self.root)
            return
        ok, msg = self.atm.deposit(amount)
        if ok:
            self._refresh_balance()
            self.amt_entry.delete(0, tk.END)
            self._set_status(msg)
            messagebox.showinfo("Deposit", msg, parent=self.root)
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    def _do_withdraw(self):
        amount, err = self._get_amount()
        if err:
            messagebox.showerror("Error", err, parent=self.root)
            return
        ok, msg = self.atm.withdraw(amount)
        if ok:
            self._refresh_balance()
            self.amt_entry.delete(0, tk.END)
            self._set_status(msg)
            messagebox.showinfo("Withdrawal", msg, parent=self.root)
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    def _open_transfer(self):
        win = tk.Toplevel(self.root)
        win.title("Transfer Funds")
        win.geometry("420x360")
        win.configure(bg=COLORS["bg"])
        win.resizable(False, False)

        tk.Frame(win, bg=COLORS["card"], pady=10).pack(fill="x")
        label(win, "Transfer Funds", "heading").pack(pady=(20, 4))

        c = card_frame(win, padx=24, pady=20)
        c.pack(padx=24, pady=8, fill="x")

        label(c, "Target Account Number").pack(anchor="w")
        tgt_e = entry_field(c)
        tgt_e.pack(pady=(2, 12))

        label(c, "Amount  $").pack(anchor="w")
        amt_e = entry_field(c)
        amt_e.pack(pady=(2, 16))

        def do_transfer():
            try:
                amount = float(amt_e.get().replace(",", ""))
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.", parent=win)
                return
            ok, msg = self.atm.transfer(tgt_e.get().strip(), amount)
            if ok:
                self._refresh_balance()
                messagebox.showinfo("Transfer", msg, parent=win)
                win.destroy()
            else:
                messagebox.showerror("Error", msg, parent=win)

        accent_button(c, "SEND TRANSFER", do_transfer, color=COLORS["accent2"]).pack(fill="x")

    def _logout(self):
        self.atm.logout()
        self.dash_frame.destroy()
        self._build_login()


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    ATMApp()