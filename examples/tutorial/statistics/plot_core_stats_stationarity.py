"""
Statistical test - Stationarity
===============================

Example using your package
"""
# Libraries
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import pyAMR
from pyamr.datasets.load import make_timeseries
from pyamr.core.stats.stationarity import StationarityWrapper

# ----------------------------
# set basic configuration
# ----------------------------
# Set pandas configuration.
pd.set_option('display.max_colwidth', 14)
pd.set_option('display.width', 150)
pd.set_option('display.precision', 4)

# Set default parameters.
mpl.rc('lines', linewidth=0.35)
mpl.rc('xtick', labelsize=6)
mpl.rc('ytick', labelsize=6)
mpl.rc('legend', fontsize=6)
mpl.rc('grid')
mpl.rc('figure')
mpl.rc('axes')
mpl.rc('font', size=7)

# Font type.
font = {
'family': 'monospace',
'weight': 'normal',
'size': 6,
}

# ----------------------------
# create data
# ----------------------------
# Constants
length = 100
offset = 100
slope = 4

# Create variables.
x = np.arange(length)
n = np.random.rand(length)

# Create timeseries.
y_n = n
y_c = np.ones(length)*offset
y_t = x*slope+n
y_ct = x*slope+offset+n*20
y_r = np.concatenate((y_ct[:50], y_ct[50:]-offset))
x_s, y_s, f_s = make_timeseries()

# ----------------------------
# Example of stationarity
# ----------------------------
# Single example
stationarity = StationarityWrapper()\
    .fit(y_r, adf_kwargs={}, kpss_kwargs={})

# Show
print("\nSeries:")
print(stationarity.as_series())

print("\nIdentifier:")
print(stationarity._identifier())


# ---------------------------
# Plot
# ---------------------------
# .. note:: Including in the timeseries variable the value
#           y_c produces the following error:
#           ValueError: cannot convert float NaN to integer.

# Create array of time series
timeseries = [y_n, y_c, y_t, y_ct, y_r, y_s]
timeseries = [y_n, y_t, y_ct, y_r, y_s]

# Create figure
fig, axes = plt.subplots(3,2, figsize=(10,8))
axes = axes.flatten()

# Loop
for i,ts in enumerate(timeseries):

    print("Stationarity... %s" % i)

    # Create stationarity wrapper.
    stationarity = StationarityWrapper().fit(x=ts)

    # Plot
    axes[i].plot(ts, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=2, linewidth=0.75,
                 label=stationarity.as_summary())

    # Set grid
    axes[i].grid(color='gray', linestyle='--',
                 linewidth=0.2, alpha=0.5)

    # Set legend
    axes[i].legend(prop=font, loc=4)

# Study of Stationarity
plt.suptitle("Study of Stationarity")

# Show
plt.show()