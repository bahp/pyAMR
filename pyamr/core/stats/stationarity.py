##############################################################################
# Author: Bernard Hernandez
# Filename: 03-main-create-sari-idxs.py
# Description : This file contains differnent statistics used in time-series.
#               What it mainly does is to format the output of tests provided
#               by external libraries and return them in a dataframe.
#
# TODO: Move it to a module.
#
###############################################################################
# Forces decimals on divisions.
from __future__ import division 

# Libraries
import sys
import numpy as np
import pandas as pd

# Import base wrapper
from pyamr.core.stats.wbase import BaseWrapper
from pyamr.core.stats.wbase import fargs

class StationarityWrapper(BaseWrapper):
  """This method....


  Types of stationarity in time-series:
    - Trend stationary
    - Seasonal stationary
    - Strictly stationary

  Refs
  ----
  [1] https://machinelearningmastery.com/time-series-data-stationary-python/
  [2]
  [3]

  """

  # --------------------------------------------------------------------------
  #                          overriden methods
  # --------------------------------------------------------------------------
  def evaluate(self, alpha=0.05, **kwargs):
    """This method initialises the series.
    """
    # Create dictionary.
    d = {}

    # Basic statistics (adfuller).
    d['adf_ct_statistic'] = self._raw['adfuller-ct'][0] 
    d['adf_ct_pvalue'] = self._raw['adfuller-ct'][1]
    d['adf_ct_nlags'] = self._raw['adfuller-ct'][2]
    d['adf_ct_nobs'] = self._raw['adfuller-ct'][3]
    for key,value in self._raw['adfuller-ct'][4].items():
      d['adf_ct_criticalvalue_%s'%key] = value

    # Basic statistics (adfuller).
    d['adf_c_statistic'] = self._raw['adfuller-c'][0] 
    d['adf_c_pvalue'] = self._raw['adfuller-c'][1]
    d['adf_c_nlags'] = self._raw['adfuller-c'][2]
    d['adf_c_nobs'] = self._raw['adfuller-c'][3]
    for key,value in self._raw['adfuller-c'][4].items():
      d['adf_c_criticalvalue_%s'%key] = value

    # Basic statistics (kpss).
    d['kpss_ct_statistic'] = self._raw['kpss-ct'][0]
    d['kpss_ct_pvalue'] = self._raw['kpss-ct'][1]
    d['kpss_ct_nlags'] = self._raw['kpss-ct'][2]
    for key,value in self._raw['kpss-ct'][3].items():
      d['kpss_ct_criticalvalue_%s'%key] = value

    # Basic statistics (kpss).
    d['kpss_c_statistic'] = self._raw['kpss-c'][0]
    d['kpss_c_pvalue'] = self._raw['kpss-c'][1]
    d['kpss_c_nlags'] = self._raw['kpss-c'][2]
    for key,value in self._raw['kpss-c'][3].items():
      d['kpss_c_criticalvalue_%s'%key] = value

    # Extra parameters.
    d['root_ct_stationary'] = d['adf_ct_pvalue']>alpha
    d['root_c_stationary'] = d['adf_c_pvalue']>alpha
    d['trend_ct_stationary'] = d['kpss_ct_pvalue']>alpha
    d['trend_c_stationary'] = d['kpss_c_pvalue']>alpha

    # Return
    return d
    
  def as_summary(self, alpha=0.05):
    """This method creates the summary to display.
    """
    # Create summary.
    summary = '      stationarity (alpha=0.05)   \n'
    summary+= '==================================\n'
    summary+= '          root           trend    \n'
    summary+= '----------------------------------\n'
    summary+= 'c  %#7s (%.3f) %#7s (%.3f)\n' % (self.root_c_stationary, 
        self.adf_c_pvalue, self.trend_c_stationary, self.kpss_c_pvalue)
    summary+= 'ct %#7s (%.3f) %#7s (%.3f)\n' % (self.root_ct_stationary,
        self.adf_ct_pvalue, self.trend_ct_stationary, self.kpss_ct_pvalue)
    summary+= '=================================='
    # Return
    return summary

 
  def fit(self, x, adf_kwargs={}, kpss_kwargs={}, **kwargs):
    """This method studies the stationarity of a given time-series.

    The parameters which can be passed to the adfuller and kpss methods
    are listed below:
    
    - adfuller_kwargs = {x, maxlag, regression, autolag, store, regresults}
    - kpss_kwargs = {x, regression, lags, store}

    @see statsmodels.tsa.stattools.adfuller
    @see statsmodels.tsa.stattoosl.kpss

    Parameters
    ----------
    x : array-like
      The time series

    adf_kwargs : dict-like
      The parameters to pass to the adfuller function

    kpss_kwargs : dict-like
      The parameters to apss to the kpss function


    Returns
    -------
    object : An StationarityWrapper objects.
    """
    # Library.
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.tsa.stattools import kpss

    # Empty the class
    self._empty()

    # In this fit a number of scenarios are going to be tested. The
    # term that varies within scenarios is regression, as such, if 
    # it is passed it will be deleted.
    adf_kwargs.pop('regression', None)
    kpss_kwargs.pop('regression', None)

    # Update the configuration
    self._config.update({'adf_%s'%k: v for k,v in adf_kwargs.items()})
    self._config.update({'kpss_%s'%k: v for k,v in kpss_kwargs.items()})

    # Initialize raw data.
    self._raw = {'x':x}

    # Compute adfuller and kpss
    self._raw['adfuller-ct'] = adfuller(x=x, regression='ct', **adf_kwargs)
    self._raw['adfuller-c'] = adfuller(x=x, regression='c', **adf_kwargs)
    self._raw['kpss-ct'] = kpss(x=x, regression='ct', **kpss_kwargs)
    self._raw['kpss-c'] = kpss(x=x, regression='c', **kpss_kwargs)

    # Evaluate the model
    if self.evaluate:
      self._result = self.evaluate()

    # Save results.
    return self
    






if __name__ == '__main__':

  # Libraries
  import matplotlib as mpl
  import matplotlib.pyplot as plt

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