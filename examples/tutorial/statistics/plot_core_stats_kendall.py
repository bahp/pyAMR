"""
Kendall
============================

The Mann-Kendall statistical test for monotonic upward or downward trend.
"""


# Libraries
import numpy as np
import pandas as pd

# Import pyAMR
from pyamr.core.stats.kendall import kendall
from pyamr.core.stats.kendall import KendallWrapper

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

# ---------------------
# Create kendall object
# ---------------------
# Create object
kendall = KendallWrapper(estimator=kendall).fit(x=y)

# Print series.
print("\n")
print(kendall.as_series())

# Print summary.
print("\n")
print(kendall.as_summary())

# Print identifier
print("\nIdentifier:")
print(kendall._identifier())