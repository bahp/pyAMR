"""
ADFuller
============================

The Augmented Dickey-Fuller test for unit root.

.. todo:: Instead of calling the ``adf.from_list_dataframe``,
          include an option in the ``grid_search`` method to
          return the result as a dataframe (to_dataframe).

"""


# Libraries
import numpy as np
import pandas as pd

# Import statsmodels
from statsmodels.tsa.stattools import adfuller

# Import pyAMR
from pyamr.core.stats.adfuller import ADFWrapper

# ----------------------------
# set basic configuration
# ----------------------------
# Set pandas configuration.
pd.set_option('display.max_colwidth', 14)
pd.set_option('display.width', 150)
pd.set_option('display.precision', 4)

# ----------------------------
# create data
# ----------------------------
# Constants
length = 100
offset = 100
slope = 10

# Create timeseries.
x = np.arange(length)
y = np.random.rand(length) * slope + offset

# ----------------------------
# create adfuller object
# ----------------------------
# Create object
adf = ADFWrapper(estimator=adfuller).fit(x=y, regression='ct')

# Print series.
print("\n")
print(adf.as_series())

# Print summary.
print("\n")
print("Standard:")
print(adf.as_summary())
print("\nVerbose:")
print(adf.as_summary(verbose=10))

# Print identifier.
print("\nIdentifier")
print(adf._identifier())

# -----------------
# Save and load
# -----------------
# File location
#fname = '../examples/saved/adfuller-sample.pickle'

# Save
#adf.save(fname=fname)

# Load
#adf = ADFWrapper().load(fname=fname)


# -----------
# Grid search
# -----------
# Create wrapper
adf = ADFWrapper(adfuller)

# Grid parameters.
grid_params = {'x': [y], 'regression': ['c','n','ct']}

# Get wrappers.
lwrappers = adf.grid_search(grid_params=grid_params, verbose=1)

# Get summary.
summary = adf.from_list_dataframe(lwrappers, flabel=True)

# Plot result.
print("\n")
print(summary.T)