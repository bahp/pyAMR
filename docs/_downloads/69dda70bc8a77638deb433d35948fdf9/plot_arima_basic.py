"""
ARIMA basic
-----------

.. todo: Explain

"""
# Import.
import sys
import warnings
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import ARIMA from statsmodels.
from statsmodels.tsa.arima_model import ARIMA

# import weights.
from pyamr.datasets.load import make_timeseries
from pyamr.core.regression.arima import ARIMAWrapper

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

# Create exogenous variable
exog = x

# ----------------------------
# fit the model
# ----------------------------
# Create specific arima model.
arima = ARIMAWrapper(estimator=ARIMA).fit( \
    endog=y[:80], order=(1,0,0), trend='c', disp=0)

# Print series
print("\nSeries:")
print(arima.as_series())

# Print summary.
print("\nSummary:")
print(arima.as_summary())

# -----------------
# Save & Load
# -----------------
# File location
#fname = '../../examples/saved/arima-sample.pickle'

# Save
#arima.save(fname=fname)

# Load
#arima = ARIMAWrapper().load(fname=fname)


# -----------------
#  Predict and plot
# -----------------
# This example shows how to make predictions using the wrapper which has
# been previously fitted. It also demonstrateds how to plot the resulting
# data for visualization purposes. It shows two different types of
# predictions:
#    - dynamic predictions in which the prediction is done based on the
#      previously predicted values. Note that for the case of ARIMA(0,1,1)
#      it returns a line.
#    - not dynamic in which the prediction is done based on the real
#      values of the time series, no matter what the prediction was for
#      those values.

# Variables.
s, e = 50, 120

# Compute predictions
preds_1 = arima.get_prediction(start=s, end=e, dynamic=False)
preds_2 = arima.get_prediction(start=s, end=e, dynamic=True)

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(8,3))

# ----------------
# Plot non-dynamic
# ----------------
# Plot truth values.
axes[0].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                markeredgecolor='k', markeredgewidth=0.5,
                markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values.
axes[0].plot(preds_1[0,:], preds_1[1,:], color='#FF0000', alpha=1.00, 
            linewidth=2.0, label=arima._identifier())

# Plot the confidence intervals.
axes[0].fill_between(preds_1[0,:], preds_1[2,:], 
                                   preds_1[3,:], 
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
axes[1].plot(preds_2[0,:], preds_2[1,:], color='#FF0000', alpha=1.00, 
            linewidth=2.0, label=arima._identifier())

# Plot the confidence intervals.
axes[1].fill_between(preds_2[0,:], preds_2[2,:], 
                                   preds_2[3,:], 
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

