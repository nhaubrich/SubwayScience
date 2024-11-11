`. get_station_data.sh` downloads the 9GB MTA subway data file, then processes it into a time-sorted CSV with one row per hour. `skim_station.py` is called along the way, which adds Fourier-encoded features for hour, day, and month, and a flag for US holidays.

(UNUSED) `get_weather_data.py` fetches hourly weather data from open-meteo's historical weather API.
