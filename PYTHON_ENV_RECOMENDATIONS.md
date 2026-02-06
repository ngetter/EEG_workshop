Below is a **clean, copy-safe addition** you can paste into **README.md**
(or keep as a separate section). No formatting traps.

---

## Python Environment Setup (using `uv`)

We recommend using **`uv`** for fast, reproducible Python environment management.

### 1. Install `uv`

#### macOS / Linux

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```bash
uv --version
```

---

### 2. Create and Activate a Virtual Environment

From the project root:

```bash
uv venv .venv
```

Activate the environment:

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

---

### 3. Install Project Dependencies

With the virtual environment activated, install all dependencies defined in
`pyproject.toml`:

```bash
uv pip install -e .
```

This will install:

* MNE and MNE-BIDS
* EEGDash and its dependencies
* Notebook tools (Jupyter / Marimo)
* All required scientific Python packages

---

### 4. Verify Installation

Run:

```bash
python env_check_instalation.py
```

If no errors are reported, the environment is ready.

---

### Notes

* Python version must be **3.9–3.11**
* MATLAB / Brainstorm are **not** installed via Python
* Use this same environment for notebooks, EEGDash, and scripts

---


