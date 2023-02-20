"""
Using WLS + ARMA
====================

.. warning:: Not working yet!

"""

"""
# Import class.
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.robust.norms as norms

from statsmodels.tsa.arima_model import ARIMA


# import weights.
from pyamr.datasets.load import make_timeseries
from pyamr.metrics.weights import SigmoidA
from pyamr.core.regression.wls import WLSWrapper
from pyamr.core.regression.wlsarma import WLSARMAWrapper

# Matplotlib options
mpl.rc('legend', fontsize=6)
mpl.rc('xtick', labelsize=6)
mpl.rc('ytick', labelsize=6)

# Set pandas configuration.
pd.set_option('display.max_colwidth', 14)
pd.set_option('display.width', 150)
pd.set_option('display.precision', 4)

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

# Create WLS + ARIMA model.
wlsarima = WLSARMAWrapper().fit(endog=y, exog=x, weights=f,
    wls_kwargs={'W': W, 'trend': 'c', 'missing': 'raise'},
     arima_kwargs={'exog': None, 'max_ar': 1,
                   'max_ma': 1, 'max_d': 0, 'ic': 'bic',
                   'order': (1,0,0)})

pred1 = wlsarima.get_prediction(start=None, end=140)
pred2 = wls.get_prediction(start=None, end=140)

endog = getattr(wlsarima._wls, 'endog')
exog = getattr(wlsarima._wls, 'exog')[:, 1]

# Create figures.
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True, sharex=True)
# Plot observations.
axes[0].plot(exog, endog, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')
axes[0].plot(pred1[0, :], pred1[1, :], color='#39ac73',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label='WLSARMA')
axes[1].plot(pred2[0, :], pred2[1, :], color='r',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label='WLS')

plt.legend()
plt.show()

import sys

sys.exit()

# Create WLS + SARIMAX model.
wlssarimax = WLSARMAWrapper().fit(endog=y, exog=x, weights=f,
                                  wls_kwargs={'W': W, 'trend': 'c', 'missing': 'raise'},
                                  sarimax_kwargs={'exog': None, 'ic': 'bic', 'max_ar': 1, 'max_ma': 1, 'max_d': 0,
                                                  'max_P': 0, 'max_D': 0, 'max_Q': 0, 'list_s': [12]})

# Create best SARIMAX model
models, sarimax = SARIMAXWrapper().fit(endog=y, ic='bic',
                                       max_ar=1, max_ma=1, max_d=1,
                                       max_P=0, max_D=0, max_Q=0,
                                       list_s=[0], return_fits=True)

# Print series.
print(wlsarima.as_series())

# Print summaries.
print(wlsarima.as_summary())
print(wlssarimax.as_summary())
print(wlsarima._arma.as_summary())
print(wlssarimax._arma.as_summary())

# -----------------
# Save & Load
# -----------------
# File location
fname_wlsarima = '../../examples/saved/wlsarima-sample.pickle'
fname_wlssarimax = '../../examples/saved/wlssarimax-sample.pickle'

# Save
wlsarima.save(fname=fname_wlsarima)
# wlssarimax.save(fname=fname_wlssarimax) (zstatespace can't be pickled)

# Load
wlsarima = WLSARMAWrapper().load(fname=fname_wlsarima)
# wlssarimax = WLSARMAWrapper().load(fname=fname_wlssarimax)

# -----------------
#  Predictions
# -----------------
# Variables.
start, end = None, None

# Compute predictions.
preds_wls = wlsarima.get_prediction(start=start, end=end, ptype='wls')
preds_arima = wlsarima.get_prediction(start=start, end=end, ptype='arma')
preds_sarimax = wlssarimax.get_prediction(start=start, end=end, ptype='arma')
preds_wlsarima = wlsarima.get_prediction(start=start, end=end)
preds_wlssarimax = wlssarimax.get_prediction(start=start, end=end)
preds_sarimax = sarimax.get_prediction(start=start, end=end)

# Create figures.
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Subplot 0
# ---------
# Plot observed values
endog = getattr(wlsarima._wls, 'endog')
exog = getattr(wlsarima._wls, 'exog')[:, 1]
axes[0].plot(exog, endog, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values (WLS-ARIMA).
axes[0].plot(preds_wlsarima[0, :], preds_wlsarima[1, :], color='#39ac73',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label=wlsarima._identifier(short=True))

# Plot confidence intervals (WLS-ARIMA)
axes[0].fill_between(preds_wlsarima[0, 3:],
                     preds_wlsarima[2, 3:],
                     preds_wlsarima[3, 3:],
                     color='#39ac73', alpha=0.1)

# Plot forecasted values (WLS-SARIMAX).
axes[0].plot(preds_wlssarimax[0, :], preds_wlssarimax[1, :], color='b',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label=wlssarimax._identifier(short=True))

# Plot confidence intervals (WLS-SARIMAX)
axes[0].fill_between(preds_wlssarimax[0, 3:],
                     preds_wlssarimax[2, 3:],
                     preds_wlssarimax[3, 3:],
                     color='b', alpha=0.1)

# Plot forecasted values and confidence intervals (SARIMAX).
axes[0].plot(preds_sarimax[0, :], preds_sarimax[1, :], color='#FF0000',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label=sarimax._identifier())

# Plot confidence intervals
axes[0].fill_between(preds_sarimax[0, 3:],
                     preds_sarimax[2, 3:],
                     preds_sarimax[3, 3:],
                     color='#FF0000', alpha=0.1)

# Subplot 1
# ---------
# Plot observed values.
axes[1].plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')

# Plot wls separately.
axes[1].plot(preds_wls[0, :], preds_wls[1, :], color='#39ac73',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label=wlsarima._wls._identifier(short=True))

axes[1].fill_between(preds_wls[0, :],
                     preds_wls[2, :],
                     preds_wls[3, :],
                     color='#39ac73', alpha=0.1)

# Plot arma separately.
axes[1].plot(preds_arima[0, :], preds_arima[1, :], color='#FF0000',
             alpha=0.95, marker='o', markersize=2, linewidth=1.0,
             markeredgewidth=0.2, markeredgecolor='k',
             label=wlsarima._arma._identifier())

axes[1].fill_between(preds_arima[0, :],
                     preds_arima[2, :],
                     preds_arima[3, :],
                     color='#FF0000', alpha=0.1)

# Grid
axes[0].grid(linestyle='--', linewidth=0.35, alpha=0.5)
axes[1].grid(linestyle='--', linewidth=0.35, alpha=0.5)

# Legend
axes[0].legend()
axes[1].legend()

# Show
plt.show()
"""