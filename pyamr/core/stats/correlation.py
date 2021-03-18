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

# Add module wrappers to sys path dynamically.
sys.path.append("../..")

# Import base wrapper
from pyamr.core.stats.wbase import BaseWrapper


class CorrelationWrapper(BaseWrapper):

  # --------------------------------------------------------------------------
  #                          overriden methods
  # --------------------------------------------------------------------------
  def evaluate(self, alpha=0.05):
    """This method set all the variables into this class.
    """
    # Create series.
    d = {}
    # Add results
    d['spearman_corr'] = self._raw['scipy.stats.spearmanr'].correlation
    d['spearman_pval'] = self._raw['scipy.stats.spearmanr'].pvalue
    d['pearson_corr'] = self._raw['scipy.stats.pearsonr'][0]
    d['pearson_pval'] = self._raw['scipy.stats.pearsonr'][1]
    d['crosscorr'] = self._raw['numpy.correlate']
    # Return
    return d
    
  def as_summary(self, alpha=0.05):
    """This method displays the summary.
    """
    # Create summary base
    summary = "         Correlation\n"
    summary+= "==============================\n"
    summary+= "Pearson:           %#11.3f\n" % self.pearson_corr
    summary+= "Spearman:          %#11.3f\n" % self.spearman_corr
    summary+= "Cross correlation: %#11.3f\n" % self.crosscorr
    summary+= "=============================="
    # Return
    return summary

  def fit(self, x1, x2, **kwargs):
    """This method computes kendall for monotonic increase

    NOTES: - scipy pvalues are not reliavble if less than 500 observations.

    Parameters
    ----------
    x1        :
    y2        :

    Returns
    -------
    object : A CorrelationWrapper objects.
    """
    # Library.
    import scipy as sp

    # Empty the class
    self._empty()

    # Update the configuration
    self._config.update(kwargs)

    # Initialize raw data
    self._raw = {} 

    # Compute correlations
    self._raw['numpy.correlate'] = np.correlate(x1, x2)
    self._raw['numpy.corrcoef'] = np.corrcoef(x1, x2)
    self._raw['scipy.stats.pearsonr'] = sp.stats.pearsonr(x1, x2)  
    self._raw['scipy.stats.spearmanr'] = sp.stats.spearmanr(x1, x2) 

    # Evaluate the model
    if self.evaluate:
      self._result = self.evaluate()

    # Save results.
    return self
    


if __name__ == '__main__':
 
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
  y1 = n*slope + offset
  y2 = n*(-slope) + offset 

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

  correlation

  # -----------------
  # Save and load
  # -----------------
  # File location
  #fname = '../examples/saved/correlation-sample.pickle'

  # Save
  #correlation.save(fname=fname)

  # Load
  #correlation = CorrelationWrapper().load(fname=fname)