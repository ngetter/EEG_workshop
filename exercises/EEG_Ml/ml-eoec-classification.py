import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from eegdash import EEGDash

    return (EEGDash,)


@app.cell
def _(EEGDash):
    eegdash = EEGDash()
    records = eegdash.find(dataset="ds002718")
    print(f"Found {len(records)} records.")
    return


@app.cell
def _():
    from eegdash import EEGDashDataset

    # Initialize the dataset for ds002718
    dataset = EEGDashDataset(
        cache_dir="./eeg_data",
        dataset="ds002718",
    )

    print(f"Found {len(dataset)} recordings in the dataset.")
    return (EEGDashDataset,)


@app.cell
def _(EEGDashDataset):
    from pathlib import Path

    # from eegdash import EEGDashDataset
    from eegdash.paths import get_default_cache_dir

    cache_folder = Path(get_default_cache_dir()).resolve()
    cache_folder.mkdir(parents=True, exist_ok=True)

    ds_eoec = EEGDashDataset(
        dataset="ds005514",
        task="RestingState",
        subject="NDARDB033FW5",
        cache_dir=cache_folder,
    )
    return (ds_eoec,)


@app.cell
def _(ds_eoec):
    from eegdash.hbn.preprocessing import hbn_ec_ec_reannotation
    from braindecode.preprocessing import (
        preprocess,
        Preprocessor,
        create_windows_from_events,
    )
    import numpy as np
    import warnings

    warnings.simplefilter("ignore", category=RuntimeWarning)


    # BrainDecode preprocessors
    preprocessors = [
        hbn_ec_ec_reannotation(),
        Preprocessor(
            "pick_channels",
            ch_names=[
                "E22",
                "E9",
                "E33",
                "E24",
                "E11",
                "E124",
                "E122",
                "E29",
                "E6",
                "E111",
                "E45",
                "E36",
                "E104",
                "E108",
                "E42",
                "E55",
                "E93",
                "E58",
                "E52",
                "E62",
                "E92",
                "E96",
                "E70",
                "Cz",
            ],
        ),
        Preprocessor("resample", sfreq=128),
        Preprocessor("filter", l_freq=1, h_freq=55),
    ]
    preprocess(ds_eoec, preprocessors)

    # Extract 2-second segments
    windows_ds = create_windows_from_events(
        ds_eoec,
        trial_start_offset_samples=0,
        trial_stop_offset_samples=int(2 * ds_eoec.datasets[0].raw.info["sfreq"]),
        preload=True,
    )
    return (windows_ds,)


@app.cell
def _(windows_ds):
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(windows_ds[2][0][0, :].transpose())  # first channel of first epoch
    plt.show()
    return


@app.cell
def _(windows_ds):
    from eegdash import features
    from eegdash.features import extract_features
    from functools import partial

    sfreq = windows_ds.datasets[0].raw.info["sfreq"]
    # Support both old (dict) and new (list) braindecode preproc metadata formats
    preproc_data = windows_ds.datasets[0].raw_preproc_kwargs
    if isinstance(preproc_data, list):
        # Find the 'filter' preprocessor in the list of dicts/objects
        filter_kwargs = {}
        for item in preproc_data:
            if isinstance(item, dict) and (
                item.get("fn") == "filter" or item.get("__class_path__") == "filter"
            ):
                filter_kwargs = item.get("kwargs", {})
                break
            elif hasattr(item, "fn") and getattr(item.fn, "__name__", "") == "filter":
                filter_kwargs = getattr(item, "kwargs", {})
                break
        filter_freqs = filter_kwargs
    else:
        filter_freqs = preproc_data.get("filter", {})
    features_dict = {
        "sig": features.FeatureExtractor(
            {
                "mean": features.signal_mean,
                "var": features.signal_variance,
                "std": features.signal_std,
                "skew": features.signal_skewness,
                "kurt": features.signal_kurtosis,
                "rms": features.signal_root_mean_square,
                "ptp": features.signal_peak_to_peak,
                "quan.1": partial(features.signal_quantile, q=0.1),
                "quan.9": partial(features.signal_quantile, q=0.9),
                "line_len": features.signal_line_length,
                "zero_x": features.signal_zero_crossings,
            },
        ),
        "spec": features.FeatureExtractor(
            preprocessor=partial(
                features.spectral_preprocessor,
                fs=sfreq,
                f_min=filter_freqs["l_freq"],
                f_max=filter_freqs["h_freq"],
                nperseg=2 * sfreq,
                noverlap=int(1.5 * sfreq),
            ),
            feature_extractors={
                "rtot_power": features.spectral_root_total_power,
                "band_power": partial(
                    features.spectral_bands_power,
                    bands={
                        "theta": (4.5, 8),
                        "alpha": (8, 12),
                        "beta": (12, 30),
                    },
                ),
                0: features.FeatureExtractor(
                    preprocessor=features.spectral_normalized_preprocessor,
                    feature_extractors={
                        "moment": features.spectral_moment,
                        "entropy": features.spectral_entropy,
                        "edge": partial(features.spectral_edge, edge=0.9),
                    },
                ),
                1: features.FeatureExtractor(
                    preprocessor=features.spectral_db_preprocessor,
                    feature_extractors={
                        "slope": features.spectral_slope,
                    },
                ),
            },
        ),
    }

    features_ds = extract_features(windows_ds, features_dict, batch_size=512)
    return (features_ds,)


@app.cell
def _(features_ds):
    features_ds.to_dataframe(include_crop_inds=True)
    return


if __name__ == "__main__":
    app.run()
