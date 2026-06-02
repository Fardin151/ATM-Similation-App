"""
Build script — converts atm_app.py into a standalone .exe (Windows)
or binary (macOS/Linux) using PyInstaller.

USAGE
-----
1. Install PyInstaller (one time):
       pip install pyinstaller

2. Run this script from the same folder as atm_app.py:
       python build.py

3. Find your executable in:
       dist/ATM Simulation/ATM Simulation.exe   (Windows)
       dist/ATM Simulation/ATM Simulation        (macOS / Linux)

NOTES
-----
- `--onedir`  produces a folder with one .exe. Faster startup than --onefile.
- `--onefile` produces a single .exe but is slower to launch (unpacks on start).
  Switch the commented lines below to use --onefile instead.
- The app saves `atm_data.json` next to the executable, so the dist folder is
  self-contained — just zip and share it.
"""

import subprocess
import sys
import os

APP_NAME   = "ATM Simulation"
MAIN_SCRIPT = "atm_app.py"

# Change to script directory so relative paths work
os.chdir(os.path.dirname(os.path.abspath(__file__)))

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--name",    APP_NAME,
    "--onedir",                  # <-- swap to --onefile for single .exe
    "--windowed",                # hides the console window (GUI app)
    "--clean",
    "--noconfirm",
    # "--icon", "atm_icon.ico",  # uncomment + add an .ico file to use a custom icon
    MAIN_SCRIPT,
]

print("=" * 60)
print(f"  Building: {APP_NAME}")
print(f"  Script  : {MAIN_SCRIPT}")
print("=" * 60)

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n✅  Build succeeded!")
    print(f"   Output → dist/{APP_NAME}/")
else:
    print("\n❌  Build failed. Check the output above for errors.")
    sys.exit(1)