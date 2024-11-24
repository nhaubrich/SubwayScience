# SubwayScience 

## Forecasting New York City's hourly subway ridership with machine learning

By Nick Haubrich and Jack Carlisle 



## Overview

With over 400 stations and up to millions of daily riders, the New York Subway is one of the largest and busiest services of its kind. Predictions of its usage in advance contain significant utility for allocating resources to different parts, whether to address short-term wear-and-tear or decade-scale improvements. The Metropolitan Transit Authority (MTA) has periodically released data on the subway's ridership as part of its Open Data Program. In this project, we apply machine learning to model and forecast the hourly ridership of the NYC subway on short and medium timescales.

:warning: Add more motivation/use cases? explicitly mention time-series 


## Dataset
The dataset consists of hourly ridership at each subway station from February 2022 to October 2024, and was obtained from [data.ny.gov](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-July-2020/wujg-7c2s/about_data). The data was preprocessed into an array with each row corresponding to an hour, with ridership for each station. Further details on this process can be found in `scripts/README.md`.

The dataset consists of 23349 hours of observations, with ridership for each of the 428 stations. The data was split into training/validation/testing intervals of 70%/10%/20%. The total ridership per hour is shown below for one month. 

![month of data](plots/monthOfData.png)

:warning: Change x-axis from hours to date-time

For forecasting, the ridership was scaled to zero mean and unit variance. Due to the cyclic time dependence, we encoded the day of week, day of the month, and month of the year as Fourier variables. Additionally, a flag for US holidays was added using python's holiday library.

## Machine Learning Forecasting
Two scenarios were considered. First, the total hourly ridership was modeled, i.e. a univariate forecast. Second, this was expanded to the multivariate case of predicting ridership for each station. Both are handled with a typical autoregressive approach where the model predicts future observations based on the past several observations plus external features.

The performance of models was evaluated on the root mean square error of the test datasets. Initial predictions from the model were fed back in to forecast the ridership multiple hours in advance. 

### Total Ridership Forecasting
For forecasting the total ridership, three model architectures were considered:
 - Linear Model
 - Dense Neural Network
 - Long Short-Term Memory Network
Hyperparameters for the deep networks were varied to obtain the local maximum in performance.
Metrics:
 - Define RMSE for X hours ahead

![total ridership forecast comparison](plots/totalRidershipWeekComparison.png)

![total ridership RMSE comparison](plots/totalRidershipRMSEComparison.png)

### Per-Station Forecasting
A per-station model requires 428 forecasts instead of a single one, resulting in a substantialincrease in computational burden. Simply feeding all station information into deep networks proved ineffective, as the increase in input variables led to overfitting and unstable extrapolations. Instead, a dense neural network that acted on each station individually was trained, implemented as a 1D CNN. Station identifiers are encoded by unique 16-dimensional vectors. (**add embedding to notebook**)

**add linear model comparison and many-to-many LSTM or NN**

![multistation RMSE](plots/multistationRMSE.png)

(plot of some stations for examples)

![map-comparison](plots/mergedMTAanimation.gif)

# Conclusions and future directions
 - Pretty effective!
 - May be way to do to LSTM what 1d CNN did to NN
 - Worst stations are near baseball stadiums or beaches...what to add?

# Environment Setup
We recommend a python virtual environment:
```
python3.11 -m venv venv/
. venv/bin/activate
pip install -r requirements.txt
```
For convenience, the notebooks download the preprocessed data from a saved source.
