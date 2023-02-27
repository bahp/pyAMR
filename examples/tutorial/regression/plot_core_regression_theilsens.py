"""
Using Theil-Sen
======================

Using Theil-Sen to fit a line to sample points.

In non-parametric statistics, the Theil–Sen estimator is a method for robustly
fitting a line to sample points in the plane (simple linear regression) by
choosing the median of the slopes of all lines through pairs of points.

.. warning: This TheilSensWrapper imports the Regression
            base from a different file. Why do we have
            wbase.py, wreg.py and wregression.py?

"""
# Libraries
import numpy as np
import pandas as pd

# Libraries.
import matplotlib.pyplot as plt

# Import pyamr
from pyamr.datasets.load import make_timeseries
from pyamr.core.regression.theilsens import TheilSensWrapper

# Set pandas configuration.
pd.set_option('display.max_colwidth', 14)
pd.set_option('display.width', 150)
pd.set_option('display.precision', 4)

def make_line(length, offset, slope):
    """Create straight series."""
    # Create timeseries.
    x = np.arange(length)
    y = np.random.rand(length) * slope + offset + x
    return x, y

# ----------------------------
# create data
# ----------------------------
# Constants
length = 100
offset = 100
slope = 10

# Create series
#x, y = make_line(length, offset, slope)

# Create timeseries data
x, y, f = make_timeseries()

# Create object
theilsens = TheilSensWrapper().fit(x=x, y=y)

# Print series.
print("\nSeries:")
print(theilsens.as_series())

# Print summary.
print("\nSummary:")
print(theilsens.as_summary())


# -----------------
#  Predictions
# -----------------
# Variables.
start, end, = None, 180

# Compute predictions.
preds = theilsens.get_prediction(start=start, end=end)

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(11,5))

# Plot truth values.
ax.plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
         markeredgecolor='k', markeredgewidth=0.5,
         markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values.
ax.plot(preds[0, :], preds[1, :], color='#FF0000', alpha=1.00,
         linewidth=2.0, label=theilsens._identifier())

# Plot the confidence intervals.
ax.fill_between(preds[0, :],
                preds[2, :],
                preds[3, :],
                color='r',
                alpha=0.1)

# Legend
plt.legend()

# ----------
# Grid search
# -----------
# Grid parameters.
grid_params = {'x': [x], 'y': [y], 'alpha': [0.05, 0.1]}

# Get summary.
summary = TheilSensWrapper().grid_search_dataframe(grid_params=grid_params)

# Plot result (drop x which is an array to improve visualization).
print("Grid Search:")
print(summary)

# Show
plt.show()