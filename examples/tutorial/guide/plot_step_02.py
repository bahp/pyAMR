"""
Step 02 - Time Series Analysis
==============================

.. warning:: Verify tests with conditions from stattools.

.. warning:: Useful references:

    - https://www.machinelearningplus.com/time-series/kpss-test-for-stationarity/
    - https://www.statsmodels.org/dev/examples/notebooks/generated/autoregressions.html

"""

###################################################################
#
# Create time series (TS)
# -----------------------
#
# First lets create an artificial series. The series has been plotted
# ad the end of the tutorial.

# ----------------------------
# create data
# ----------------------------
# Import specific
from pyamr.datasets.load import make_timeseries

# Create timeseries data
x, y, f = make_timeseries()


###################################################################
#
# Pearson correlation coefficient
# -------------------------------
#
# It measures the linear correlation between two variables with a value within the range
# [-1,1]. Coefficient values of -1, 0 and 1 indicate total negative linear correlation, no
# linear correlation and total positive correlation respectively. In this study, the
# coefficient is used to assess whether or not there is a linear correlation between the
# number of observations (susceptibility test records) and the computed resistance index.

# -------------------------------
# Pearson correlation coefficient
# -------------------------------
# Import pyAMR
from pyamr.core.stats.correlation import CorrelationWrapper

# Create object
correlation = CorrelationWrapper().fit(x1=y, x2=f)

# Print summary.
print("\n")
print(correlation.as_summary())

#######################################################################################
#
# Augmented Dickey-Fuller test
# ----------------------------
# The augmented Dickey–Fuller test (ADF) was used to determine the presence of a unit root.
# When the other roots of the characteristic function lie inside the unit circle the first
# difference of the process is stationary. Due to this property, these are also called
# difference-stationary processes
#
# https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html

# ----------------------------
# ADFuller
# ----------------------------
# Import statsmodels
from statsmodels.tsa.stattools import adfuller

# Import pyAMR
from pyamr.core.stats.adfuller import ADFWrapper

# Create wrapper
adf = ADFWrapper(adfuller).fit(x=y, regression='ct')

print("\n")
print(adf.as_summary())


#######################################################################################
#
# Kwiatkowski-Phillips-Schmidt-Shin test
# --------------------------------------
#
# https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.kpss.html

# ----------------------------
# Kpss
# ----------------------------


###################################################################
#
# Trend and stationarity in TS
# ----------------------------
#
# An analysis of stationarity around a trend was carried out to identify time series
# satisfying the assumptions posed by ARIMA. The augmented Dickey–Fuller test (ADF) was
# used to determine the presence of a unit root. When the other roots of the characteristic
# function lie inside the unit circle the first difference of the process is stationary. Due
# to this property, these are also called difference-stationary processes. Since the absence
# of unit root is not a proof of non-stationarity, the Kwiatkowski–Phillips–Schmidt–Shin
# (KPSS) test was used to identify the existence of an underlying trend which can also be
# removed to obtain a stationary process. These are called trend-stationary processes. In
# both, unit-root and trend-stationary processes, the mean can be increasing or decreasing
# over time; however, in the presence of a shock, trend-stationary processes revert to this
# mean tendency in the long run (deterministic trend) while unit-root processes have a
# permanent impact (stochastic trend). The significance level of the tests was set to 0.05.

# ----------------------------
# Stationarity
# ----------------------------
# Generic
import matplotlib.pyplot as plt

# Import pyAMR
from pyamr.core.stats.stationarity import StationarityWrapper

# Define kwargs
adf_kwargs = {'maxlag':12, 'autolag':'BIC'}
kpss_kwargs = {}

# Compute stationarity
stationarity = StationarityWrapper().fit(x=y,
    adf_kwargs=adf_kwargs, kpss_kwargs=kpss_kwargs)

# Print summary.
print("\n")
print(stationarity.as_summary())


# ----------------
# plot
# ----------------
# Font type.
font = {
    'family': 'monospace',
    'weight': 'normal',
    'size': 10,
}

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(10, 4))

# Plot truth values.
ax.plot(y, color='#A6CEE3', alpha=0.5, marker='o',
         markeredgecolor='k', markeredgewidth=0.5,
         markersize=4, linewidth=0.75,
         label=stationarity.as_summary())

# Format axes
ax.grid(color='gray', linestyle='--', linewidth=0.2, alpha=0.5)
ax.legend(prop=font, loc=4)

# Addd title
plt.suptitle("Study of Stationarity")

plt.show()