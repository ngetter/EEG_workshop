# EEG Workshop – Technical Requirements for Participants

This document describes the required hardware, software, and data setup for the EEG workshop.
The workshop uses **Brainstorm (UI only)**, **MNE + MNE-BIDS**, **EEGDash**, and **Python notebooks**.

---

## 1. Hardware Requirements

* Personal laptop (Windows, macOS, or Linux)
* Minimum **16 GB RAM** (32 GB recommended)
* Minimum **30 GB free disk space** (SSD strongly recommended)
* GPU optional (not required)

---

## 2. Operating System

One of the following:

* Windows 10/11 (64-bit)
* macOS 12 or newer
* Linux (Ubuntu 20.04+ recommended)

---

## 3. MATLAB + Brainstorm (UI use only)

Participants must have **Brainstorm available**, using **one** of the following options.

### Option A — MATLAB Installation

* MATLAB **R2022a or newer**
* Installed toolboxes:

  * Signal Processing Toolbox
  * Statistics & Machine Learning Toolbox
* Brainstorm (latest stable version)
  * [download - brainstorm_260206.zip](https://neuroimage.usc.edu/bst/download.php)
* Valid MATLAB license (academic license sufficient)

### Option B — MATLAB Runtime (MCR, no license)

* MATLAB Compiler Runtime (MCR) compatible with the Brainstorm version
* Brainstorm standalone distribution
  *   [download - brainstorm_260206.zip](https://neuroimage.usc.edu/bst/download.php)
* No MATLAB coding required (GUI workflows only)

---

## 4. Python Environment (mandatory)

* **Python 3.9–3.11**
* Environment manager:

  * `conda` or
  * `venv` - preferable

### Required Python packages

* `mne`
* `mne-bids`
* `numpy`
* `scipy`
* `pandas`
* `matplotlib`

### Strongly recommended

* `autoreject`
* `pyvista`


## 5. In a different ML environment EEGDash (mandatory)

* Prefere instalation on a separate env. 
* EEGDash installed locally
  [https://eegdash.org](https://eegdash.org)
* Used for:

  * EEG dataset ingestion and management
  * feature extraction
  * machine-learning workflows
  * model evaluation and comparison
* Requirements:

  * Compatible Python environment
  * Modern web browser (Chrome or Firefox)
  * Ability to run local services (localhost)

---

## 6. Notebook Environment (mandatory)

One of the following:

* Jupyter Notebook / JupyterLab
* Marimo - preffered [https://marimo.io/](https://marimo.io/)

Requirements:

* Must run in the **same Python environment** as MNE, MNE-BIDS, and EEGDash
* Used for:

  * BIDS inspection and validation
  * preprocessing demonstrations
  * feature extraction
  * ML experiments

---

## 7. EEG Data Requirements

Participants may bring their own EEG data.

Accepted formats:

* **All EEG formats supported by both Brainstorm and MNE**, including (but not limited to):

  * EDF / BDF
  * BrainVision
  * EEGLAB `.set`
  * FIF
  * CNT, EGI, Nicolet, and related formats

Additional requirements:

* Data will be organized or converted to **BIDS** during the workshop
* Metadata must include:

  * channel names
  * sampling rate
  * reference information

Backup datasets will be provided.

---

## 8. General Software

* Git
* ZIP / unzip utility
* PDF reader
* Code editor (VS Code recommended)

---

## 9. Network & Permissions

* Administrator rights to install software
* Stable internet connection
* Ability to run local servers and services

---


