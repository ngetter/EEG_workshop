# EEG Workshop – Technical Requirements for Participants

This document describes the required hardware, software, and data setup for the EEG workshop.  
The workshop uses **Brainstorm (UI)**, **MNE + MNE-BIDS**, **EEGDash**, and **Python notebooks**.

---

## 1. Hardware Requirements
- Personal laptop (Windows, macOS, or Linux)
- Minimum **16 GB RAM** (32 GB recommended)
- Minimum **30 GB free disk space** (SSD strongly recommended)
- GPU optional (not required)

---

## 2. Operating System
One of the following:
- Windows 10/11 (64-bit)
- macOS 12 or newer
- Linux (Ubuntu 20.04+ recommended)

---

## 3. MATLAB + Brainstorm (UI use only)

Participants must have Brainstorm available using **one** of the following options.

### Option A — MATLAB Installation
- MATLAB R2022a or newer
- Installed toolboxes:
  - Signal Processing Toolbox
  - Statistics & Machine Learning Toolbox
- Brainstorm (latest stable version)
- Valid MATLAB license (academic license sufficient)

### Option B — MATLAB Runtime (MCR, no license)
- MATLAB Compiler Runtime (MCR) compatible with the Brainstorm version
- Brainstorm standalone distribution
- No MATLAB coding required (GUI workflows only)

---

## 4. Python Environment (mandatory)
- Python 3.9–3.11
- Environment manager:
  - `conda` or
  - `venv`

### Required Python packages
- `mne`
- `mne-bids`
- `numpy`
- `scipy`
- `pandas`
- `matplotlib`

### Strongly recommended
- `autoreject`
- `pyvista`

Pre-work validation:
```bash
python -c "import mne, mne_bids; print(mne.__version__)"
