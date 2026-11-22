DATA 608 Story 5 | 1995–2024
Run with Python, pandas, numpy and matplotlib:
  python story5_analysis.py PATH_TO_RAW_CSV_FOLDER PATH_TO_OUTPUT_FOLDER

Inputs:
  GLB.Ts+dSST.csv — NASA GISTEMP v4 annual J-D land–ocean temperature anomaly, °C relative to 1951–1980.
  https://data.giss.nasa.gov/gistemp/data_v4.html
  ibtracs.since1980.list.v04r01.csv — NOAA NCEI IBTrACS v04r01, modern era subset.
  https://www.ncei.noaa.gov/products/international-best-track-archive
  1950-2024_actual_tornadoes.csv — NOAA SPC, redistributed by Aerostratospheric.
  https://huggingface.co/datasets/aerostratospheric/spc-tornado-history

Metrics:
  Tropical cyclones: one main-track storm per basin and season, based on peak US-agency
  sustained wind while classified as tropical. If agency status is blank, IBTrACS tropical
  nature is used. A peak of 64 knots qualifies; 96 knots or higher counts as strong.
  These basin counts do not describe all tropical cyclones globally.
  Tornadoes: count US reports after grouping rows sharing year, ID, date, time, state
  and start coordinates. Among rated reports only, F/EF2 or higher counts as strong.
  Unknown ratings do not count as weak. F and EF ratings and detection practices
  have changed over time. The strength measures differ across storm families.
  *_strong_share columns are proportions from zero to one.

Pearson r summarizes linear association. The detrended result removes a separate
straight-line time trend from each series before computing r. Neither establishes
causality. The plotted lines are descriptive fits, not forecasts.
