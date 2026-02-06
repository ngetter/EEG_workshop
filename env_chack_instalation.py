"""
EEG Workshop – Environment Validation Cell

Run this cell in your notebook.
It will report clear PASS / FAIL messages for all required components.
"""

import sys
import importlib
import shutil
import socket

errors = []
warnings = []

def check(condition, ok_msg, err_msg):
    if condition:
        print(f"✅ {ok_msg}")
    else:
        print(f"❌ {err_msg}")
        errors.append(err_msg)

def check_import(pkg, name=None):
    name = name or pkg
    try:
        importlib.import_module(pkg)
        print(f"✅ Python package '{name}' available")
    except Exception as e:
        msg = f"Python package '{name}' NOT available ({e})"
        print(f"❌ {msg}")
        errors.append(msg)

print("=== EEG Workshop Environment Check ===\n")

# Python version
py_ok = (3, 9) <= sys.version_info < (3, 12)
check(
    py_ok,
    f"Python version OK ({sys.version.split()[0]})",
    f"Python version NOT supported ({sys.version.split()[0]}), require 3.9–3.11"
)

# Core Python packages
for pkg in [
    "mne",
    "mne_bids",
    "numpy",
    "scipy",
    "pandas",
    "matplotlib",
]:
    check_import(pkg)

# Optional but recommended
for pkg in ["autoreject", "pyvista"]:
    try:
        importlib.import_module(pkg)
        print(f"⚠️ Optional package '{pkg}' available")
    except Exception:
        warnings.append(f"Optional package '{pkg}' not installed")

# Notebook environment
check(
    "ipykernel" in sys.modules or shutil.which("jupyter"),
    "Notebook environment detected",
    "Notebook environment NOT detected"
)

# EEGDash check (import-level)
try:
    import eegdash  # type: ignore
    print("✅ EEGDash package importable")
except Exception:
    warnings.append("EEGDash package not importable (check installation)")

# Localhost / port availability
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    sock.close()
    print("✅ Localhost networking OK")
except Exception as e:
    errors.append(f"Localhost networking issue: {e}")

print("\n=== Summary ===")
if errors:
    print("❌ Environment NOT ready")
    print("Issues:")
    for e in errors:
        print(f" - {e}")
else:
    print("🎉 Environment READY for the EEG workshop")

if warnings:
    print("\nWarnings:")
    for w in warnings:
        print(f" - {w}")
