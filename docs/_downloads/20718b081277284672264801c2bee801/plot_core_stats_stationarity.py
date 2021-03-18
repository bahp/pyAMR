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

# ----------------------------
# create stationarity objects
# ----------------------------
stationarity_n = StationarityWrapper().fit(x=y_n)
stationarity_c = StationarityWrapper().fit(x=y_c)
stationarity_t = StationarityWrapper().fit(x=y_t)
stationarity_r = StationarityWrapper().fit(x=y_r)
stationarity_ct = StationarityWrapper().fit(x=y_ct,
                adf_kwargs={'maxlag':12, 'autolag':'BIC'})

# Print series.
print("\n")
print(stationarity_ct.as_series())

# Print summary.
print("\n")
print(stationarity_ct.as_summary())

# Print identifier.
print("\n")
print(stationarity_ct._identifier())


# ----------------
# plot
# ----------------
# Create figure
fig, axes = plt.subplots(3,2, figsize=(10,4))
axes = axes.flatten()

# Plot truth values.
axes[0].plot(y_n, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=2, linewidth=0.75,
             label=stationarity_n.as_summary())

axes[1].plot(y_c, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=2, linewidth=0.75,
             label=stationarity_c.as_summary())

# Plot truth values.
axes[2].plot(y_t, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=2, linewidth=0.75,
             label=stationarity_t.as_summary())

# Plot truth values.
axes[3].plot(y_ct, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=2, linewidth=0.75,
             label=stationarity_ct.as_summary())

# Plot truth values.
axes[4].plot(y_r, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=2, linewidth=0.75,
             label=stationarity_r.as_summary())

# Add grid
for ax in axes:
    ax.grid(color='gray', linestyle='--', linewidth=0.2, alpha=0.5)

# Add legend
for ax in axes:
    ax.legend(prop=font, loc=2)

# Study of Stationarity
plt.suptitle("Study of Stationarity")

# -----------------
# Save and load
# -----------------
# File location
#fname = '../examples/saved/stationarity-sample.pickle'

# Save
#stationarity_ct.save(fname=fname)

# Load
#stationarity_ct = StationarityWrapper().load(fname=fname)

# Show
plt.show()