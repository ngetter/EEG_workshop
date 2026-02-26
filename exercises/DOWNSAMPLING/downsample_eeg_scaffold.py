import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pathlib
    import matplotlib.pyplot as plt
    from eegdash import EEGDash
    from eegdash.dataset import DS003775
    return DS003775, EEGDash, mo, pathlib, plt


@app.cell
def _(mo):
    mo.md(
        r"""
# EEG Downsampling Exercise (Scaffold)

In this exercise, you will:
1. Add target downsampling frequencies to a list.
2. Add the line that actually downsamples the EEG signal.
3. Compare the plotted signal after downsampling.

Target frequencies for this exercise: **250 Hz, 128 Hz, 30 Hz**.

The code below intentionally contains TODO markers for students to complete.
"""
    )
    return


@app.cell
def _(DS003775, EEGDash, pathlib):
    # Connect to EEGDash and download/load one dataset recording.
    eegdash = EEGDash()
    eeg_data = pathlib.Path("./eeg_data/")
    dataset = DS003775(cache_dir=eeg_data)
    raw_eeg = dataset.datasets[0].raw
    return raw_eeg


@app.cell
def _():
    target_sfreqs = [
        # TODO: Add required frequencies here, e.g. 250, 128, 30
    ]
    return target_sfreqs


@app.cell
def _(mo, plt, raw_eeg, target_sfreqs):
    if not target_sfreqs:
        mo.md(
            "Add values to `target_sfreqs` to continue. Required: `250, 128, 30`."
        )
        return

    plots = []
    for target_sfreq in target_sfreqs:
        raw_ds = raw_eeg.copy().load_data()

        # TODO: Add the downsampling line here.
        # Example:
        # raw_ds.resample(sfreq=target_sfreq, npad="auto")

        data = raw_ds.get_data(picks=[0])[0]
        t = raw_ds.times

        fig, ax = plt.subplots(figsize=(10, 2.8))
        ax.plot(t, data, linewidth=0.8)
        ax.set_title(
            f"Target: {target_sfreq} Hz | Actual sfreq: {raw_ds.info['sfreq']:.1f} Hz"
        )
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude (V)")
        ax.grid(True, alpha=0.3)
        plots.append(mo.as_html(fig))
        plt.close(fig)

    mo.vstack(
        [
            mo.md(
                "After completing TODOs, verify that actual sampling frequencies match your targets."
            ),
            *plots,
        ]
    )
    return


if __name__ == "__main__":
    app.run()
