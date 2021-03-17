"""
Regression - WLS search
----------------------------

The example below loads a portion of the culture dataset and creates the 
pipeline to remove outliers, imput missing data, address the class imbalance 
and scale the data features accordingly. After this, a number of estimators 
are trained and tested (see wrappers and grids). The results such as the
estimators (pickle) and metrics (csv) re stored in the specified path.

@see core
@see xxx
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

# -----------------------------
# Example II
# -----------------------------
# This example performs grid search on a number of possible configurations
# of the WLSWrapper. In particular, it tests the effect of different 
# objects to compute the weights from the frequencies. It presents both
# the resulting pandas dataframe and also a figure.

# Configuration
# -------------
# This variable contains the weight functions to test. Note that in 
# the norms module there are other options such as [norms.HuberT(), 
# norms.Hampel(), norms.TrimmedMean(), norms.TukeyBiweight(), 
# norms.AndreWave(), norms.RamsayE()]
w_func = [
    norms.LeastSquares(),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[10, 90]),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[25, 75]),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[25, 90]),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[40, 50])]

# The grid search parameters.
grid_params = [
    # {'exog': [x], 'endog': [y], 'trend': ['c']},
    {'exog': [x], 'endog': [y], 'trend': ['c'], 'weights': [f], 'W': w_func}
]

# Grid search
# ------------
# Perform grid search.
summary = WLSWrapper(estimator=sm.WLS) \
    .grid_search(grid_params=grid_params)

# Show grid results
# ..todo: It is weird to create an WLSWrapper jut to
#         be able to use themethod from_list_dataframe.
#         try to implemented separately.
print("\nGrid search:")
print(WLSWrapper().from_list_dataframe(summary).T)

# Prediction
# ----------
# Variables.
start, end = 10, 150

# Create figure
fig, axes = plt.subplots(1, 3, figsize=(10, 5))

# Plot truth values.
axes[0].plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')

# Plot frequencies
axes[0].bar(x, f, color='gray', alpha=0.7, label='Frequency')

# For each of the models in summary
for i, model in enumerate(summary):

    # Compute predictions.
    preds = model.get_prediction(start=start, end=end)

    # Plot forecasted values.
    axes[0].plot(preds[0, :], preds[1, :],
                 linewidth=1.0,
                 label=model._identifier(short=True))

    # Plot the confidence intervals.
    axes[0].fill_between(preds[0, :],
                         preds[2, :],
                         preds[3, :],
                         alpha=0.1)

    # Plot weights assigned to each observation
    axes[1].plot(model.weights, marker='o', alpha=0.5,
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=4, linewidth=0.00,
                 label=model._identifier(short=True))

    # Plot weights converter (W) functions.
    if model.W is not None:
        axes[2].plot(np.linspace(0, 1, 100),
                     model.W.weights(np.linspace(0, 1, 100)),
                     label=model._identifier(short=True))

# Grid.
axes[0].grid(linestyle='--', linewidth=0.35, alpha=0.5)
axes[1].grid(linestyle='--', linewidth=0.35, alpha=0.5)
axes[2].grid(linestyle='--', linewidth=0.35, alpha=0.5)

# Legend.
axes[0].legend(loc=0)
axes[1].legend(loc=0)
axes[2].legend(loc=0)

# Tight layout
plt.tight_layout()

# Show.
plt.show()
