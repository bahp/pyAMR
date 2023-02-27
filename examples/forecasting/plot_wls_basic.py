"""
WLS - Basic
-------------------

Basic example using Weighted Least Squares to fit a time series.

"""
# Import class.
import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.robust.norms as norms

# import weights.
from pyamr.datasets.load import make_timeseries
from pyamr.core.regression.wls import WLSWrapper
from pyamr.metrics.weights import SigmoidA

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

# Create method to compute weights from frequencies
W = SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0)

# Note that the function fit will call M.weights(weights) inside and will
# store the M converter in the instance. Therefore, the code execute is
# equivalent to <weights=M.weights(f)> with the only difference being that
# the weight converter is not saved.
wls = WLSWrapper(estimator=sm.WLS).fit( \
    exog=x, endog=y, trend='c', weights=f,
    W=W, missing='raise')

# Print series.
print("\nSeries:")
print(wls.as_series())

# Print regression line.
print("\nRegression line:")
print(wls.line(np.arange(10)))

# Print summary.
print("\nSummary:")
print(wls.as_summary())

# -----------------
# Save & Load
# -----------------
# File location
#fname = '../../examples/saved/wls-sample.pickle'

# Save
#wls.save(fname=fname)

# Load
#wls = WLSWrapper().load(fname=fname)

# -------------
#  Example I
# -------------
# This example shows how to make predictions using the wrapper and how
# to plot the resultin data. In addition, it compares the intervales
# provided by get_prediction (confidence intervals) and the intervals
# provided by wls_prediction_std (prediction intervals). 
#
# To Do: Implement methods to compute CI and PI (see regression).

# Variables.
start, end = None, 180

# Compute predictions (exogenous?). It returns a 2D array
# where the rows contain the time (t), the mean, the lower
# and upper confidence (or prediction?) interval.
preds = wls.get_prediction(start=start, end=end)


# Create figure
fig, ax = plt.subplots(1, 1, figsize=(11,5))

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
ax.fill_between(preds[0, :], preds[2, :],
                             preds[3, :],
                             color='r',
                             alpha=0.1)

# Legend
plt.legend()

# Show
plt.show()

