"""
Regression - SARIMAX search
----------------------------

.. note: Explain

"""
# Import.
import sys
import warnings
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import sarimax
from statsmodels.tsa.statespace.sarimax import SARIMAX

# import weights.
from pyamr.datasets.load import make_timeseries
from pyamr.core.regression.sarimax import SARIMAXWrapper

# Filter warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)

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

# Variables.
s, e = 50, 120

# -------------------------------
# create arima model
# -------------------------------
# This example shows how to use auto to find the best overall model using
# a particular seletion criteria. It also demonstrates how to plot the 
# resulting data for visualization purposes. Note that it only prints
# the top best classifier according to the information criteria.

# Find the best arima model (bruteforce).
models, best = SARIMAXWrapper(estimator=SARIMAX) \
    .auto(endog=y[:80], ic='bic',
                        max_ar=2,
                        max_ma=3,
                        max_d=1,
                        max_P=1,
                        max_D=0,
                        max_Q=1,
                        list_s=[12],
                        return_fits=True)

# Sort the list (from lower to upper)
models.sort(key=lambda x: x.bic, reverse=False)

# Summary
summary = SARIMAXWrapper().from_list_dataframe(models)

# Show summary
print("\nSummary:")
print(summary[['sarimax-order',
               'sarimax-seasonal_order',
               'sarimax-trend', 
               'sarimax-aic', 
               'sarimax-bic']])

# -------------------------------
# plot results
# -------------------------------
# Create figure
fig, axes = plt.subplots(3,3, figsize=(10,6))
axes = axes.flatten()

# Loop for the selected models
for i,estimator in enumerate(models[:9]):

  # Show information
  print("%2d. Estimator (bic=%.2f): %s " % \
    (i, estimator.bic, estimator._identifier()))

  # Get the predictions
  preds = estimator.get_prediction(start=s, end=e, dynamic=False)

  # Plot truth values.
  axes[i].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                  markeredgecolor='k', markeredgewidth=0.5,
                  markersize=5, linewidth=0.75, label='Observed')

  # Plot forecasted values.
  axes[i].plot(preds[0,:], preds[1,:], color='#FF0000', alpha=1.00, 
               linewidth=2.0, label=estimator._identifier())
  
  # Plot the confidence intervals.
  axes[i].fill_between(preds[0,:], preds[2,:], 
                                   preds[3,:], 
                                   color='#FF0000', 
                                   alpha=0.25)

  # Configure axes
  axes[i].legend(loc=3)
  axes[i].grid(True, linestyle='--', linewidth=0.25)

# Set superior title
plt.suptitle("Non-dynamic predictions for SARIMAX")

# Show
plt.show()
