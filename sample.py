import marimo

__generated_with = "0.0.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import importlib
    return importlib, mo


@app.cell
def _(importlib, mo):
    def check_module(name):
        try:
            module = importlib.import_module(name)
            version = getattr(module, "__version__", "installed")
            return "OK", str(version)
        except Exception as exc:
            return "FAIL", str(exc).splitlines()[0]

    mne_status, mne_info = check_module("mne")
    eegdash_status, eegdash_info = check_module("eegdash")
    mo.md(
        f"""
# Hello, world from marimo!

## Environment checks
- `mne`: **{mne_status}** ({mne_info})
- `eegdash`: **{eegdash_status}** ({eegdash_info})
"""
    )
    return


if __name__ == "__main__":
    app.run()
