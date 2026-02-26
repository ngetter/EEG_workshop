import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pathlib
    import re
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import mne
    import mne_bids
    from fooof import FOOOF
    from eegdash import EEGDash
    from eegdash.dataset import DS003775

    return DS003775, EEGDash, mne, mne_bids, mo, pathlib, re


@app.cell
def _(mo):
    mo.md(r"""
    # BIDS + EEGDash Demo: PSD and FOOOF

    This demo:
    1. Lists all subjects in the dataset.
    2. Lists all tasks in the dataset.
    3. Lists all sessions in the dataset.
    4. Loads one eyes-closed file and one eyes-open file by **task** or **session**.
    5. Computes PSD for both files.
    6. Runs FOOOF for both PSDs and displays summary info.
    """)
    return


@app.cell
def _(DS003775, EEGDash, pathlib):
    # Download/load DS003775 into local cache.
    _ = EEGDash()
    eeg_data = pathlib.Path("./eeg_data/")
    eeg_data.mkdir(parents=True, exist_ok=True)
    dash_data = DS003775(cache_dir=eeg_data)
    bids_root = eeg_data / "ds003775"
    raw = dash_data.datasets[0].raw
    raw.info
    return (bids_root,)


@app.cell
def _(bids_root, mne_bids):
    subjects = sorted(mne_bids.get_entity_vals(bids_root, "subject"))
    tasks = sorted(mne_bids.get_entity_vals(bids_root, "task"))
    sessions = sorted(mne_bids.get_entity_vals(bids_root, "session"))
    return sessions, subjects, tasks


@app.cell
def _(mo, sessions, subjects, tasks):
    s_txt = ", ".join(subjects) if subjects else "None found"
    t_txt = ", ".join(tasks) if tasks else "None found"
    ses_txt = ", ".join(sessions) if sessions else "None found"
    mo.md(
        f"""
    ## Dataset inventory
    - Subjects: {s_txt}
    - Tasks: {t_txt}
    - Sessions: {ses_txt}
    """
    )
    return


@app.cell
def _(bids_root, re):
    pattern = re.compile(
        r"sub-(?P<subject>[^_]+)_ses-(?P<session>[^_]+)_task-(?P<task>[^_]+)_eeg\.(?P<ext>edf|bdf|fif|set)$"
    )
    records = []
    for fpath in bids_root.glob("sub-*/ses-*/eeg/*_eeg.*"):
        match = pattern.search(fpath.name)
        if not match:
            continue
        rec = match.groupdict()
        rec["path"] = str(fpath)
        records.append(rec)
    return (records,)


@app.cell
def _():
    selection_mode = "task"
    # Set to "task" or "session"

    eyes_closed_selector = "resteyesc"
    eyes_open_selector = "resteyeso"
    # If selection_mode == "task": set task names above.
    # If selection_mode == "session": set session labels (e.g., "t1", "t2") above.
    return eyes_closed_selector, eyes_open_selector, selection_mode


@app.cell
def _(eyes_closed_selector, eyes_open_selector, records, selection_mode):
    def _is_eyes_closed(task_name):
        t = task_name.lower()
        return ("eyesc" in t) or ("closed" in t)

    def _is_eyes_open(task_name):
        t = task_name.lower()
        return ("eyeso" in t) or ("open" in t)

    def _select_record(state, selector):
        state_fn = _is_eyes_closed if state == "closed" else _is_eyes_open
        for rec in records:
            if not state_fn(rec["task"]):
                continue
            if selection_mode == "task" and rec["task"] == selector:
                return rec
            if selection_mode == "session" and rec["session"] == selector:
                return rec
        return None

    rec_closed = _select_record("closed", eyes_closed_selector)
    rec_open = _select_record("open", eyes_open_selector)
    return rec_closed, rec_open


@app.cell
def _(mne, rec_closed, rec_open):
    if rec_closed is None or rec_open is None:
        raw_closed = None
        raw_open = None
    else:
        raw_closed = mne.io.read_raw(rec_closed["path"], preload=True, verbose=False)
        raw_open = mne.io.read_raw(rec_open["path"], preload=True, verbose=False)
    return


@app.cell
def _(mo, rec_closed, rec_open):
    if rec_closed is None or rec_open is None:
        mo.md(
            "Could not find both eyes-closed and eyes-open files. Check `selection_mode` and selector values."
        )
    else:
        mo.md(
            f"""
    ## Selected files
    - Eyes closed: `{rec_closed["path"]}`
    - Eyes open: `{rec_open["path"]}`
    """
        )
    return


app._unparsable_cell(
    r"""
    if raw_closed is None or raw_open is None:
        return None, None, None, None

    psd_closed = raw_closed.copy().crop(tmin=1, tmax=30).compute_psd(fmin=1, fmax=45)
    p_closed, freqs = psd_closed.get_data(return_freqs=True)
    p_closed_mean = np.mean(p_closed, axis=0)

    psd_open = raw_open.copy().crop(tmin=1, tmax=30).compute_psd(fmin=1, fmax=45)
    p_open, _ = psd_open.get_data(return_freqs=True)
    p_open_mean = np.mean(p_open, axis=0)
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    if freqs is None:
        mo.md("PSD not computed yet.")
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(freqs, 10 * np.log10(p_closed_mean), label="Eyes closed")
    ax.plot(freqs, 10 * np.log10(p_open_mean), label="Eyes open")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power (dB)")
    ax.set_title("PSD comparison")
    ax.grid(True, alpha=0.3)
    ax.legend()
    mo.as_html(fig)
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    if freqs is None:
        return None, None

    fm_closed = FOOOF(peak_width_limits=[1, 12], max_n_peaks=6, verbose=False)
    fm_open = FOOOF(peak_width_limits=[1, 12], max_n_peaks=6, verbose=False)
    fm_closed.fit(freqs, p_closed_mean, [1, 45])
    fm_open.fit(freqs, p_open_mean, [1, 45])
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    if fm_closed is None or fm_open is None:
        mo.md("FOOOF not computed yet.")
        return

    summary = pd.DataFrame(
        [
            {
                "recording": "eyes_closed",
                "aperiodic_offset": fm_closed.aperiodic_params_[0],
                "aperiodic_exponent": fm_closed.aperiodic_params_[1],
                "n_peaks": len(fm_closed.peak_params_),
                "r_squared": fm_closed.r_squared_,
                "error": fm_closed.error_,
            },
            {
                "recording": "eyes_open",
                "aperiodic_offset": fm_open.aperiodic_params_[0],
                "aperiodic_exponent": fm_open.aperiodic_params_[1],
                "n_peaks": len(fm_open.peak_params_),
                "r_squared": fm_open.r_squared_,
                "error": fm_open.error_,
            },
        ]
    )
    mo.vstack([mo.md("## FOOOF summary"), summary])
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
