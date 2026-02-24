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
    return (pathlib,)


@app.cell
def _(pathlib):
    from eegdash.dataset import DS003775


    EEG_DATA = pathlib.Path('./eeg_data/')
    BIDS_DATASET = 'DS003775'
    dataset = DS003775(cache_dir=EEG_DATA)
    # Get the raw object of the first recording
    raw_eeg = dataset.datasets[0].raw
    print(raw_eeg.info)
    return (raw_eeg,)


@app.cell
def _(raw_eeg):
    # from mne_bids import BIDSPath, read_raw_bids
    # bids_path = mne_bids.BIDSPath(datatype='eeg', 
    #                               extension='set', 
    #                               subject='019', 
    #                               task='RestingState', 
    #                               root=EEG_DATA / BIDS_DATASET)

    # raw_eeg_spect = mne_bids.read_raw_bids(bids_path=bids_path)
    raw_eeg.copy().crop(1,30).compute_psd(fmax =40, method="welch").plot()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
