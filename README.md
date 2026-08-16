# Grodan — NRE Digital Twin Dashboard

A Streamlit application that turns Grodan's Nutrient Refurbishment Efficiency (NRE) lab test
results into an interactive 3D digital twin of a stone wool slab. It was built as a proof of
concept during a digital transformation internship, to help R&D and Sales compare the water
content (WC) and electrical conductivity (EC) behavior of different slab products, replacing
the static 2D graphs previously used for this purpose.

## What it does

- Renders a 3D model of a slab for two selected products side by side, using [PyVista](https://pyvista.org/)
  (via [stpyvista](https://github.com/edsaac/stpyvista)) for the 3D rendering inside Streamlit.
- Interpolates EC and WC sensor readings (8 positions x 4 heights per slab) into a smooth 3D
  surface for each product, colored by value.
- Lets the user step through the 25 irrigation moments recorded during an 8-hour NRE test with
  a time-stamp slider.
- Plots EC/WC uniformity (standard deviation over height and over length) with Plotly bar charts,
  for a quantitative comparison alongside the 3D view.
- Optionally shows a short auto-generated text commentary comparing the two selected slabs.

## Requirements

- Python 3.9+
- The packages in `requirements.txt`:

  ```bash
  pip install -r requirements.txt
  ```

## Data setup

This app does not ship with any lab data or product logos — those are Grodan's internal
assets and are intentionally excluded from this repository (see `.gitignore`).

To run it locally, point the app at a folder containing the expected data via the
`GRODAN_DATA_ROOT` environment variable:

```bash
export GRODAN_DATA_ROOT="/path/to/your/Grodan/data"      # macOS/Linux
# or
$env:GRODAN_DATA_ROOT = "C:\path\to\your\Grodan\data"     # Windows PowerShell
```

If unset, it defaults to a `data/` folder next to `Grodan_main_noGPT.py`. That folder is
expected to contain:

```
data/
├── Grodan_logo.jpg
├── Rockwool_logo.jpg
├── Grodan Product Logos/
│   └── <product logo>.png            # one per slab product
└── Data and codes/
    ├── <Brand>/<Product>/EC/*.csv    # 25 CSVs per product, one per irrigation moment
    ├── <Brand>/<Product>/WC/*.csv
    └── pyvista/gifs2/output_comparison/*.gif   # optional pre-rendered comparison GIFs
```

Each EC/WC CSV is expected to have a `Height (mm)` column plus `EC Position 1..8` (or
`WC Position 1..8`) columns, matching the 8 sensor positions along the slab and 4 measured
heights, one file per irrigation moment during the test.

## Running

```bash
streamlit run Grodan_main_noGPT.py
```

## Project background

This dashboard was developed as part of a digital transformation internship at Grodan (part
of Rockwool Group), focused on exploring digital twin technology for visualizing NRE test
results. It's a proof-of-concept front end; the roadmap for turning it into a production tool
(standardized data pipeline, hosted deployment, ML-based interpolation/prediction) is described
in the accompanying internship report and is out of scope for this repo.

## Notes

- This is a local-only PoC — there is no authentication or hosted deployment here.
- Never commit API keys, credentials, or Grodan's proprietary lab data to this repository.
  Configuration like `GRODAN_DATA_ROOT` should be supplied via environment variables, not
  hardcoded in the source.
