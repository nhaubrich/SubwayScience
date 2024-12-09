## Data Processing
The primary data processing script is `get_station_data.sh`, which downloads the 9GB MTA subway data file and processes it into a time-sorted CSV with one row per hour. `skim_station.py` is called along the way to accumulate data for each hour and create features. 

Several time features are included through Fourier encoding. That is, for each period of length $P$, two features are added:

$$
\mathrm{X_P} = \cos(2\pi\frac{\mathrm{t}}{P}),\\
\mathrm{Y_P} = \cos(2\pi\frac{\mathrm{t}}{P}).
$$

The periods encoded were day of week ($P=7$), day of the month ($P=31$), and month of the year ($P=12$).

A binary flag denoting federal holidays was computed from the [holidays](https://pypi.org/project/holidays/) package.

(UNUSED) `get_weather_data.py` fetches hourly weather data from the [Open-Meteo](https://open-meteo.com/en/docs) historical weather API. To align with the MTA hourly subway data, the extra fall daylight savings hours are skipped.
