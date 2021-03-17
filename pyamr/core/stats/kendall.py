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
from wbase import BaseWrapper


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------

def kendall(x):  
  """   
  Parameters
  ----------
  x     : a vector of data
  alpha : significance level (0.05 default)

  Returns
  -------
  trend : tells the trend (increasing, decreasing or no trend)
  h     : True (if trend is present) or False (if trend is absence)
  p     : p value of the significance test
  z     : normalized test statistics 
  """
  # Libraries.
  from scipy.stats import norm

  # Compute n.
  n = len(x)

  # calculate S 
  s = 0
  for k in range(n-1):
      for j in range(k+1,n):
          s += np.sign(x[j] - x[k])

  # calculate the unique data
  unique_x = np.unique(x)
  g = len(unique_x)

  # calculate the var(s)
  if n == g: # there is no tie
      var_s = (n*(n-1)*(2*n+5))/18
  else: # there are some ties in data
      tp = np.zeros(unique_x.shape)
      for i in range(len(unique_x)):
          tp[i] = sum(unique_x[i] == x)
      var_s = (n*(n-1)*(2*n+5) + np.sum(tp*(tp-1)*(2*tp+5)))/18

  # calculate z
  if s>0:      z = (s - 1)/np.sqrt(var_s)
  elif s == 0: z = 0
  elif s<0:    z = (s + 1)/np.sqrt(var_s)

  # Check
  if np.isnan(s): return [None, None]

  # calculate the p_value
  p = 2*(1-norm.cdf(abs(z))) # two tail test

  # Return
  return [p, z]

class KendallWrapper(BaseWrapper):
  """
  """

  # --------------------------------------------------------------------------
  #                             new methods
  # --------------------------------------------------------------------------
  def trend_exists(self, alpha):
    """This method returns a boolean with the stationarity outocme.

    Parameters
    ----------
    alpha : float
      The significance level

    Returns
    -------
    """
    # Libraries.
    from scipy.stats import norm
    # Check.
    if self._raw[1] is None: return None
    # Return
    return abs(self._raw[1]) > norm.ppf(1-alpha/2) # abs(z)

  def trend_direction(self, alpha):
    """This method returns the trend direction.

    Parameters
    ----------
    alpha : float
      The significance level

    Returns
    -------
    """
    # Libraries.
    from scipy.stats import norm
    # Check
    if self._raw is None: return "failed"
    # Compute h
    h = abs(self._raw[1]) > norm.ppf(1-alpha/2) 
    # Trends
    z = self._raw[1]
    if (z<0) and h:   return 'decreasing'
    elif (z>0) and h: return 'increasing'
    else:             return 'no trend'

  # --------------------------------------------------------------------------
  #                           override methods
  # --------------------------------------------------------------------------
  def evaluate(self, alpha=0.05, **kwargs):
    """Evaluates the model.
    """
    # Create series
    d = {}

    # Add results
    d['m_pvalue'] = self._raw[0]
    d['m_z'] = self._raw[1]
    d['m_trend_existence'] = self.trend_exists(alpha)
    d['m_trend_direction'] = self.trend_direction(alpha)

    # Return
    return d
    
  def as_summary(self, alpha=0.05):
    """This method displays the summary.
    """
    # Create summary base
    summary = '     kendall test (monotonic)  \n'
    summary+= "==================================\n"
    summary+= "statistic (z):   %#17.3f\n" % self.m_z
    summary+= "pvalue (manual): %#17.5f\n" % self.m_pvalue
    summary+= "trend exists:    %17s\n" % self.trend_exists(alpha)
    summary+= "trend direction: %17s\n" % self.trend_direction(alpha)
    summary+= "=================================="
    # Return
    return summary








if __name__ == '__main__':
 
 
  # Libraries
  import pandas as pd

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
  print "\n"
  print kendall.as_series()

  # Print summary.
  print "\n"
  print kendall.as_summary()

  # Print identifier
  print "\n"
  print kendall._identifier()
 
  # -----------------
  # Save and load
  # -----------------
  # File location
  #fname = '../examples/saved/kendall-sample.pickle'

  # Save
  #kendall.save(fname=fname)

  # Load
  #kendall = KendallWrapper().load(fname=fname)