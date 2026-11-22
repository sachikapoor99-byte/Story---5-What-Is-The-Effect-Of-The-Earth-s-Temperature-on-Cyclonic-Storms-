# Story 5: Do warmer years bring more or stronger storms?
Sachi Kapoor | DATA 608 | 1995–2024

[View slides (PDF)](Story5_Presentation.pdf) 

## Audience and storytelling framework
Designed for a high-school earth science class. The three-act framework is explained on slide 2:
1. Setup: invite a prediction and show the temperature record.
2. Test: compare frequency and strength separately, explaining that each dot represents one year.
3. Resolution: give students three questions to use when evaluating a storm headline.

Simple language, original labeled storm schematics, consistent colors, larger chart labels and separate definitions of frequency and strength support this audience. Slide 7 visibly states that weak correlations in these records do not mean warming has no effect on storms.

## Findings and limits
All six Pearson correlations were weak (absolute r below 0.21) for annual global temperature versus the chosen regional storm counts and strong-storm shares. Detrended correlations were also weak. These are descriptive associations, not causal estimates or evidence that climate change has no effect on storms. The analysis does not measure rainfall, storm surge, rapid intensification, local sea temperature or every basin worldwide.

Intensity is represented by the share reaching a threshold, not an individual storm's average intensity: peak US-agency wind >=96 knots among qualifying hurricanes/typhoons, and F/EF2+ among rated U.S. tornado reports. See README.txt for processing details and reporting limitations.

## Files and reproduction
- story5_analysis.py: processing, correlations and storm charts.
- story5_annual_metrics.csv: 30 annual observations.
- story5_correlations.csv: raw and detrended correlations.
- README.txt: sources and methods.

Install pandas, numpy and matplotlib. Download the three raw input CSV files listed in README.txt, then run:
    python story5_analysis.py RAW_DATA_FOLDER OUTPUT_FOLDER

The raw IBTrACS file is too large for an ordinary GitHub upload; download it from NOAA.

## Presentation recording
Add your unlisted YouTube recording link here after recording.
