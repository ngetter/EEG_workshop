# EEG Workshop

Welcome to the EEG Workshop repository.

This repository accompanies a hands-on EEG workshop using **Brainstorm (UI only)**, **MNE + MNE-BIDS**, **EEGDash**, and **Python notebooks**.

Please complete the steps below **before Day 1** to ensure your environment is ready.

---

## 1. Read the Technical Requirements

Before doing anything else, carefully read:

**TECHNICAL_REQUIREMENTS.md**

This document describes the required hardware, operating system, and software setup for the workshop.

---

## 2. Verify Your Python Environment

Run the environment check script to validate your Python installation and dependencies:

```bash
python env_check_instalation.py
```

This script checks:

* Python version compatibility
* Required Python packages (MNE, MNE-BIDS, etc.)
* Optional recommended packages
* Basic local networking availability

If the script reports errors, resolve them **before the workshop**.

---

## 3. Verify Brainstorm (MATLAB)

You must be able to launch **Brainstorm**.

What to check:

* Start Brainstorm (via MATLAB or standalone)
* Confirm that the **Brainstorm splash screen / logo appears**

No MATLAB coding is required for the workshop.
This step only verifies that the Brainstorm **GUI launches correctly**.

---

## 4. Quick Start

If you want the fastest confirmation that everything works:

1. Activate your Python environment
2. Open a notebook (Jupyter or Marimo)
3. Run the following cell:

```python
import mne
import mne_bids
print("MNE version:", mne.__version__)
print("MNE-BIDS loaded successfully")
```

4. Launch Brainstorm and wait for the main window to appear
5. Start EEGDash and confirm the web interface loads in your browser

If all steps succeed, your system is ready.

---

## 5. Day-1 Sanity Checks

On the morning of **Day 1**, please confirm the following.

### Python

* Python environment activates without errors
* Notebook opens and executes cells
* `mne` and `mne-bids` import successfully

### Brainstorm

* Brainstorm starts normally
* Main GUI window appears
* No license or runtime errors are shown

### EEGDash

* EEGDash service starts
* Web UI is accessible via browser (localhost)
* No immediate startup errors

### Data Access

* Workshop datasets are accessible on disk
* At least one dataset loads in either MNE or Brainstorm

---

## 6. You Are Ready When

You are ready to attend the workshop if:

* You have read **TECHNICAL_REQUIREMENTS.md**
* `env_check_instalation.py` runs without errors
* Brainstorm launches successfully
* Notebook and EEGDash both run

If any step fails, please fix it in advance or contact the workshop organizers.

---

We look forward to working with you.

---

