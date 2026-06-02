# ◈ ATM Simulation

A feature-rich ATM desktop app built with Python and Tkinter. Supports multiple user accounts, persistent data storage, transaction history, fund transfers, and PIN management — all wrapped in a clean dark-themed UI.

---

## Screenshots

> Run the app to see the dark-themed login screen, dashboard, and transaction history window.
<img width="577" height="788" alt="image" src="https://github.com/user-attachments/assets/9a4c7134-fb54-4055-980a-04e1381824ac" />
<img width="579" height="788" alt="image" src="https://github.com/user-attachments/assets/37abc763-f88e-46ab-ad49-0db3551f9a94" />
<img width="420" height="389" alt="image" src="https://github.com/user-attachments/assets/80845e54-5be7-4bbd-8a96-e2c999a55138" />
<img width="763" height="549" alt="image" src="https://github.com/user-attachments/assets/8b1258c0-3144-4b97-9075-50d6a3571023" />
<img width="406" height="370" alt="image" src="https://github.com/user-attachments/assets/ef6c0b20-63a1-4de7-a860-f4735bc5fd98" />

---

## Features

- 🎨 **Modern dark UI** — custom color system, hover effects, and clean typography using Consolas
- 👥 **Multiple user accounts** — 3 demo accounts included, each with their own balance and PIN
- 🧾 **Transaction history** — scrollable popup showing all past transactions with timestamps and color-coded types
- 💸 **Fund transfers** — send money between accounts; both sides get a transaction record
- 🔐 **Change PIN** — securely update your PIN with current PIN verification
- 💾 **Persistent data** — all balances and history auto-save to `atm_data.json` and reload on next launch
- 📦 **Exportable as `.exe`** — package into a standalone executable with PyInstaller (no Python required to run)

---

## Demo Accounts

| Account | PIN  | Name           | Starting Balance |
|---------|------|----------------|-----------------|
| 1001    | 1234 | Alice Johnson  | $5,000.00       |
| 1002    | 4321 | Bob Smith      | $2,500.00       |
| 1003    | 0000 | Charlie Brown  | $750.00         |

---

## Getting Started

### Requirements

- Python 3.8 or higher
- Tkinter (included with most Python installations)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/atm-simulation.git
cd atm-simulation

# Run the app
python atm_app.py
```

> No third-party packages are required. The app uses only Python's standard library.

---

## File Structure

```
atm-simulation/
├── atm_app.py       # Main application (all logic + UI)
├── build.py         # PyInstaller build script (optional)
├── atm_data.json    # Auto-generated on first transaction
└── README.md
```

**`atm_app.py`** — The entire app lives here, organized into clear sections:
- `ATM` class — core banking logic (deposit, withdraw, transfer, PIN change)
- UI helper functions — reusable styled widgets (buttons, cards, inputs)
- `ATMApp` class — login screen + dashboard
- Standalone popup functions — history window, transfer dialog, change PIN dialog

**`atm_data.json`** — Created automatically when you make your first transaction. Stores all account data including balances and full transaction history. Delete this file to reset back to defaults.

**`build.py`** — Only needed if you want to export a `.exe`. See section below.

---

## How to Use

### Login
Enter an account number and PIN from the demo accounts table above, then click **SIGN IN** or press Enter.

### Dashboard
| Button | Action |
|--------|--------|
| DEPOSIT | Add funds to your account |
| WITHDRAW | Take funds from your account |
| TRANSFER | Send money to another account |
| HISTORY | View all past transactions |
| CHANGE PIN | Update your 4-digit PIN |
| SIGN OUT | Return to the login screen |

Type an amount in the **Amount $** field before clicking Deposit or Withdraw.

---

## Building a Standalone `.exe`

To share the app with someone who doesn't have Python installed:

```bash
# Install PyInstaller (one time)
pip install pyinstaller

# Build the executable
python build.py
```

The output will be in `dist/ATM Simulation/`. Share the entire folder — the `.exe` inside is the app.

> **Note:** The `atm_data.json` file will be saved next to the `.exe` when running the packaged version, so data persists between sessions.

---

## Customizing Accounts

To change the default accounts, edit the `DEFAULT_ACCOUNTS` dictionary near the top of `atm_app.py`:

```python
DEFAULT_ACCOUNTS = {
    "1001": {"pin": "1234", "name": "Alice Johnson", "balance": 5000.00, "transactions": []},
    # Add or edit accounts here
}
```

> If `atm_data.json` already exists, delete it first — the app loads from the file on startup, so changes to `DEFAULT_ACCOUNTS` only take effect when no save file is present.

---

## Built With

- [Python](https://www.python.org/) — core language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework (standard library)
- [PyInstaller](https://pyinstaller.org/) — optional, for `.exe` packaging

---

## License

This project is open source and available under the [MIT License](LICENSE).
