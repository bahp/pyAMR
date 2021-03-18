"""
Statistical test - Correlation
==============================

Example using your package
"""


# Libraries
import numpy as np
import pandas as pd

# Import statsmodels
from statsmodels.tsa.stattools import adfuller

# Import pyAMR
from pyamr.core.stats.correlation import CorrelationWrapper

# ----------------------------
# set basic configuration
# ----------------------------
# Set pandas configuration.
pd.set_option('display.max_colwidth', 80)
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
n = np.random.rand(length)
y1 = n * slope + offset
y2 = n * (-slope) + offset

# ----------------------------
# create correlation object
# ----------------------------
# Create object
correlation = CorrelationWrapper().fit(x1=y1, x2=y2)

# Print series.
print("\n")
print(correlation.as_series())

# Print summary.
print("\n")
print(correlation.as_summary())

# Print identifier.
print("\nIdentifier:")
print(correlation._identifier())
