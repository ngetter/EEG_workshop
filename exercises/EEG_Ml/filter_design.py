import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pathlib
    import pandas as pd
    import mne
    import mne_bids # for best practice
    import json 
    from eegdash import EEGDash
    from eegdash import EEGDashDataset
    # Connect to the public database
    eegdash = EEGDash()


    from eegdash.dataset import DS003775


    EEG_DATA = pathlib.Path('./eeg_data/')
    dataset = DS003775(cache_dir=EEG_DATA)
    # Get the raw object of the first recording
    raw_eeg = dataset.datasets[1].raw
    print(raw_eeg.info)


    return mne, mo, raw_eeg


@app.cell
def _():
    # bids_path = mne_bids.BIDSPath(datatype='eeg', extension='set', subject='019', task='RestingState', root=EEG_DATA / BIDS_DATASET)
    # print(bids_path)
    # coordsystem = {
    #     "EEGCoordinateSystem": "Other",
    #     "EEGCoordinateUnits": "mm",
    #     "EEGCoordinateSystemDescription": "Coordinate system not specified in original dataset"
    # }
    # coordsystem_path = pathlib.Path(bids_path).parent / 'sub-019_task-FaceRecognition_coordsystem.json'

    # with open(coordsystem_path, 'w') as f:
    #     json.dump(coordsystem, f, indent=4)
    # raw_eeg = mne_bids.read_raw_bids(bids_path=bids_path)
    return


@app.cell
def _(mo, raw_eeg):
    import matplotlib.pyplot as plt

    plots = []
    for lp in range(100, 10, -20):
        fig = raw_eeg.copy().crop(1,30).load_data().filter(l_freq=1.0, h_freq=lp).compute_psd(fmax =120).plot()
        fig.suptitle(f"Low-pass: {lp} Hz")
        plots.append(mo.as_html(fig))
        plt.close(fig)


    mo.vstack(plots)

    return


@app.cell
def _(mne, mo, raw_eeg):
    import numpy as np

    sfreq = raw_eeg.info['sfreq']  # get sampling frequency from your data

    # Create filter coefficients
    filt = mne.filter.create_filter(
        data=None,          # or pass your data array
        sfreq=sfreq,
        l_freq=5,         # highpass cutoff (None to skip)
        h_freq=None,        # lowpass cutoff (None to skip)
        method='fir',       # 'fir' or 'iir'
        fir_window='hamming',
        filter_length='15s',
        phase='zero',       # 'zero', 'zero-double', 'minimum'
    )

    pf = mne.viz.plot_filter(filt, sfreq=sfreq)
    def apply_filter_to_raw(filt, raw, crop):
        data = raw.crop(*crop).get_data()
        # Apply coefficients to data
        filtered_data = mne.filter.notch_filter  # ← not this
    
        # Use _overlap_add_filter directly (what MNE uses internally)
        filtered_data = mne.filter._overlap_add_filter(data, filt)
    
        # Inject back into a Raw object
        raw_filtered = raw_eeg.copy().crop(*crop).load_data()
        raw_filtered._data[:] = filtered_data
        return raw_filtered
    psd_filtered = apply_filter_to_raw(filt, raw_eeg.copy(), (1,30)).compute_psd(fmax=60).plot()
    mo.vstack([pf, psd_filtered])

    return


if __name__ == "__main__":
    app.run()
