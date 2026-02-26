import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pathlib
    import mne
    from eegdash import EEGDash
    from eegdash.dataset import DS003775
    return DS003775, EEGDash, mne, mo, pathlib


@app.cell
def _(mo):
    mo.md(
        r"""
# EEG Montage + Re-reference Exercise (Scaffold)

In this exercise, you will:
1. Load EEG data from EEGDash.
2. List available built-in montages in MNE.
3. Copy and paste the correct montage name into the TODO field.
4. Re-reference the data by choosing one of:
   - average reference
   - single-channel reference

This notebook is intentionally scaffolded. Complete the TODO sections.
"""
    )
    return


@app.cell
def _(DS003775, EEGDash, pathlib):
    # Same data-loading pattern used in exercises/BIDS_DATA/read-bids.py
    _ = EEGDash()
    eeg_data = pathlib.Path("./eeg_data/")
    dataset = DS003775(cache_dir=eeg_data)
    raw_eeg = dataset.datasets[0].raw.copy().load_data()
    return raw_eeg


@app.cell
def _(mne, mo):
    montage_names = mne.channels.get_builtin_montages()
    montage_text = "\n".join(f"- `{name}`" for name in montage_names)
    mo.md(
        f"""
## Available built-in montages

Copy one montage name from this list into `selected_montage_name`.

{montage_text}
"""
    )
    return montage_names


@app.cell
def _():
    selected_montage_name = ""
    # TODO: Paste a montage name from the list above.
    # Example: selected_montage_name = "standard_1020"
    return selected_montage_name


@app.cell
def _(mne, mo, raw_eeg, selected_montage_name):
    if not selected_montage_name:
        mo.md("Set `selected_montage_name` before continuing.")
        return

    raw_with_montage = raw_eeg.copy()
    montage = mne.channels.make_standard_montage(selected_montage_name)
    raw_with_montage.set_montage(montage, on_missing="warn")

    mo.md(
        f"""
## Montage applied
- Selected montage: `{selected_montage_name}`
- Channels in raw: `{len(raw_with_montage.ch_names)}`
"""
    )
    return raw_with_montage


@app.cell
def _():
    reference_mode = ""
    # TODO: Choose one: "average" or "single"

    reference_channel = ""
    # TODO: If reference_mode == "single", set one channel name, e.g. "Cz"
    return reference_channel, reference_mode


@app.cell
def _(mo, raw_with_montage, reference_channel, reference_mode):
    if reference_mode not in {"average", "single"}:
        mo.md('Set `reference_mode` to either `"average"` or `"single"`.')
        return

    raw_reref = raw_with_montage.copy()

    # TODO: Add the re-referencing line that matches your selected mode.
    # Example for average:
    # raw_reref.set_eeg_reference("average")
    #
    # Example for single channel:
    # raw_reref.set_eeg_reference(ref_channels=[reference_channel])

    preview = raw_reref.copy().crop(tmin=1, tmax=6)
    fig_preview = preview.plot(n_channels=10, show=False, scalings="auto")

    psd = raw_reref.copy().crop(tmin=1, tmax=30).compute_psd(fmin=1, fmax=45)
    fig_psd = psd.plot(show=False)

    bands = {
        "Delta (1-4 Hz)": (1, 4),
        "Theta (4-8 Hz)": (4, 8),
        "Alpha (8-13 Hz)": (8, 13),
        "Beta (13-30 Hz)": (13, 30),
        "Gamma (30-45 Hz)": (30, 45),
    }
    fig_topo = psd.plot_topomap(bands=bands, show=False)

    mo.vstack(
        [
            mo.md(
                f"Applied reference mode: `{reference_mode}` (channel: `{reference_channel}`)"
            ),
            mo.md("### Time-series preview"),
            mo.as_html(fig_preview),
            mo.md("### PSD"),
            mo.as_html(fig_psd),
            mo.md("### Topomap (5 frequency bands)"),
            mo.as_html(fig_topo),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
