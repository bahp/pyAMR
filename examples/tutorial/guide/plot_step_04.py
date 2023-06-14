"""
Step 04 - TSA to estimate trends
================================

.. warning:: Pending!

In this example, we will learn about important concepts such as time series
decomposition, autocorrelation, moving averages, and forecasting methods from
basic linear square models to more complex approaches such as ARIMA (AutoRegressive
Integrated Moving Average). We will also explore various statistical tools
commonly used for time series analysis, empowering you to harness the power of
time-dependent data and extract meaningful information from it. Get ready to embark
on a brief yet exciting journey into the world of time series analysis!

"""

##############################################################
#
# The diagram in Figure 4.7 describes the methodology suggested to estimate secular
# trends in AMR from susceptibility test data. Since data corruption might occur in clinical
# environments, those susceptibility test records wrongly reported (human or device errors)
# or duplicated should be discarded. The remaining records are often divided into combinations
# (tuples defined by sample type or specimen, pathogen and antimicrobial) for which a resistance
# time series signal needs to be generated using either independent or overlapping time intervals
# (see xxx). The time series were linearly interpolated to fill sporadic missing values. No
# additional filters or preprocessing steps were applied. An analysis of stationarity around
# a trend was carried out to identify interesting combinations and regression
# analysis was used to quantify its tendency
#
#
# .. image:: ../../../_static/imgs/sart-diagram.png
#   :width: 600
#   :align: center
#   :alt: Diagram
#
# |
#
# The linear model (see Equation 4.3) has been selected to quantify resistance tendency
# for several reasons: (i) the development of resistance in pathogens is an evolutionary
# response to the selective pressure of antimicrobials, hence large variations in short
# periods (e.g. consecutive days or months) are not expected (ii) the slope parameter can
# be directly translated to change over time increasing its practicability and (iii) the
# offset parameter is highly related with the overall resistance. Hence, the response variable
# in regression analysis (resistance index) is described by the explanatory variable (time).
# The slope (m) ranges within the interval [-1,1] where sign and absolute value capture
# direction and rate of change respectively. The unit of the slope is represented by ∆y/∆x.
#
# - **Least Squares Regression**
#
#   The optimization problem in ordinary least squares or ``OLS`` regression minimizes the least
#   square errors to find the best fitting model. Ordinary least squares - OLS - assumes
#   identical weights (wi) and independently distributed residuals with a normal distribution.
#   It is frequent to observe that some residuals might have higher variance than others,
#   meaning that those observations are effectively less certain. To contemplate such variability,
#   weighted linear squares or ``WLS`` regression (see Equation 4.4) applies a weighting
#   function to the residuals. The confidence of the computed resistance index (observed
#   variable) relies on the number of susceptibility test records manipulated. Hence, the
#   sigmoid function has been used to define weights proportional to the population size.
#
#   .. warning:: Include equation and/or external reference.
#
# - **Auto Regressive Integrated Moving Average** or ``ARIMA``
#
#   An autoregressive integrated moving average (ARIMA) model is a generalization of an
#   autoregressive moving average (ARMA) model which can be also applied in scenarios
#   where data show evidence of non-stationarity. The autoregressive (AR) part expresses
#   the variable of interest (resistance index) as a function of past values of the variable.
#   The moving average (MA) indicates that the regression error is a linear combination of
#   error terms which occurred contemporaneously and at various times in the past. An
#   ARIMA(p,d,q) model is described by: p is the number of autoregressive terms,
#   d is the number of differences needed for stationarity and q is the
#   number of lagged forecast errors.
#
#   .. warning:: Include equation and/or external reference.
#
#   The interpretation of the parameter µ depends on the ARIMA model used for the
#   fitting. In order to estimate the linear trend, it was interesting to consider exclusively
#   MA models so that the expected value of µ was the mean of the one-time differenced
#   series; that is, the slope coefficient of the un-differenced series. The Bayesian information
#   criterion (BIC) was used to select the best ARIMA(0,1,q) model, being the one with the
#   lowest BIC the preferred.
#
#

#%%
# Lets load the libraries and create the time series.

# Import
import pandas as pd

# Import class.
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.robust.norms as norms

# import weights.
from pyamr.datasets.load import make_timeseries

# Filter warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------
# set basic configuration
# ----------------------------
# Matplotlib options
mpl.rc('legend', fontsize=6)
mpl.rc('xtick', labelsize=6)
mpl.rc('ytick', labelsize=6)

# Set pandas configuration.
pd.set_option('display.max_colwidth', 14)
pd.set_option('display.width', 150)
pd.set_option('display.precision', 4)

# ----------------------------
# create data
# ----------------------------
# Create timeseries data
x, y, f = make_timeseries()

##################################################################
# Example using WLS
# -----------------
# Libraries
from pyamr.core.regression.wls import WLSWrapper
from pyamr.metrics.weights import SigmoidA

# Create method to compute weights from frequencies
W = SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0)

# Note that the function fit will call M.weights(weights) inside and will
# store the M converter in the instance. Therefore, the code execute is
# equivalent to <weights=M.weights(f)> with the only difference being that
# the weight converter is not saved.
wls = WLSWrapper(estimator=sm.WLS).fit( \
    exog=x, endog=y, trend='c', weights=f,
    W=W, missing='raise')

#%%
# All information can be seen as a series

# Print series.
print("\nSeries:")
print(wls.as_series())

#%%
# Or a summary

# Print summary.
print("\nSummary:")
print(wls.as_summary())

#%%
# The regression line can be seen as

# Print regression line.
print("\nRegression line:")
print(wls.line(np.arange(10)))

#%%
# Let's see how to make predictions using the wrapper and how
# to plot the result in data. In addition, it compares the intervals
# provided by ``get_prediction`` (confidence intervals) and the intervals
# provided by ``wls_prediction_std`` (prediction intervals).

# -----------------------------
# Predictions
# -----------------------------
# Variables.
start, end = None, 180

# Compute predictions (exogenous?). It returns a 2D array
# where the rows contain the time (t), the mean, the lower
# and upper confidence (or prediction?) interval.
preds = wls.get_prediction(start=start, end=end)


# Create figure
fig, ax = plt.subplots(1, 1, figsize=(11,5))

# -----------------------------
# Plotting confidence intervals
# -----------------------------
# Plot truth values.
ax.plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
           markeredgecolor='k', markeredgewidth=0.5,
           markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values.
ax.plot(preds[0,:], preds[1, :], color='#FF0000', alpha=1.00,
             linewidth=2.0, label=wls._identifier(short=True))

# Plot the confidence intervals.
ax.fill_between(preds[0, :],
                preds[2, :],
                preds[3, :],
                color='r',
                alpha=0.1)

# Legend
plt.legend()

# Show
plt.show()


##################################################################
# Example using ARIMA
# -------------------

#%%
# .. note:: Since we are using arima, we should have checked for stationarity!
#

# Libraries
# Import ARIMA from statsmodels.
from statsmodels.tsa.arima.model import ARIMA
# Import ARIMA wrapper from pyamr.
from pyamr.core.regression.arima import ARIMAWrapper

# ----------------------------
# create data
# ----------------------------
# Create timeseries data
x, y, f = make_timeseries()

# Create exogenous variable
exog = x

# ----------------------------
# fit the model
# ----------------------------
# Create specific arima model.
arima = ARIMAWrapper(estimator=ARIMA).fit( \
 endog=y[:80], order=(1,0,0), trend='c', disp=0)

#%%
# All information can be seen as a series

# Print series
print("\nSeries:")
print(arima.as_series())

#%%
# Or a summary

# Print summary.
print("\nSummary:")
print(arima.as_summary())

#%%
# Lets see how to make predictions using the wrapper which has been previously
# fitted. It also demonstrates how to plot the resulting data for visualization
# purposes. It shows two different types of predictions: (i) **dynamic predictions**
# in which the prediction is done based on the previously predicted values. Note
# that for the case of ARIMA(0,1,1) it returns a line and (ii) **not dynamic** in
# which the prediction is done based on the real values of the time series, no
# matter what the prediction was for those values.

# ----------------
# Predictions
# ----------------
# Variables.
s, e = 50, 120

# Compute predictions
preds_1 = arima.get_prediction(start=s, end=e, dynamic=False)
preds_2 = arima.get_prediction(start=s, end=e, dynamic=True)

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(8, 3))

# ----------------
# Plot non-dynamic
# ----------------
# Plot truth values.
axes[0].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values.
axes[0].plot(preds_1[0, :], preds_1[1, :], color='#FF0000', alpha=1.00,
             linewidth=2.0, label=arima._identifier())

# Plot the confidence intervals.
axes[0].fill_between(preds_1[0, :], preds_1[2, :],
                     preds_1[3, :],
                     color='#FF0000',
                     alpha=0.25)

# ------------
# Plot dynamic
# ------------
# Plot truth values.
axes[1].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values.
axes[1].plot(preds_2[0, :], preds_2[1, :], color='#FF0000', alpha=1.00,
             linewidth=2.0, label=arima._identifier())

# Plot the confidence intervals.
axes[1].fill_between(preds_2[0, :], preds_2[2, :],
                     preds_2[3, :],
                     color='#FF0000',
                     alpha=0.25)

# Configure axes
axes[0].set_title("ARIMA non-dynamic")
axes[1].set_title("ARIMA dynamic")

# Format axes
axes[0].grid(True, linestyle='--', linewidth=0.25)
axes[1].grid(True, linestyle='--', linewidth=0.25)

# Legend
axes[0].legend()
axes[1].legend()

# Show
plt.show()
