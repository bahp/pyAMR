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
import statsmodels.api as sm

class SigmoidA:

  def __init__(self, r=200, g=0.5, offset=0.0, scale=1.0,
      percentiles=None, thresholds=None):
    """This function initialises the parameters.

    Parameters
    ----------
    r           : affects the ....
    g           : affects the ....
    offset      : to offset the final sigmoid.
    scale       : to scale the [0,1] sigmoid to the new range.
    percentiles :
    thresholds  :
    """
    self.r = r
    self.g = g
    self.offset = offset
    self.scale = scale
    self.percentiles = percentiles
    self.thresholds = thresholds

  # ---------------------------------------------------------------------------
  #                            HELPER METHODS
  # ---------------------------------------------------------------------------
  def _identifier(self, short=True):
    """This methods describes de model."""
    # Return short description.
    if short:
      per = 'N' if self.percentiles is None else self.percentiles
      ths = 'N' if self.thresholds is None else self.thresholds
      return "Sig(%s, %s)" % (per, ths)
    # Return full description.
    return "%s(r=%s, g=%s, offset=%s, sc=%s, per=%s, ths=%s)" % \
      (self.__class__.__name__, self.r, self.g, self.offset, self.scale, 
        self.percentiles, self.thresholds)

  # ---------------------------------------------------------------------------
  #                                SIGMOID
  # ---------------------------------------------------------------------------
  def approximated_sigmoid(self, x, x_curves=None):
    """This function computes the approximated sigmoid.

    Note: The approximated sigmoid is defined within the interval [0,1].

    .. note: Produces a RuntimeWarning: invalid value encountered in
             true_divide z = (x-cmin) / (cmax-cmin) when the parameter
             x has always the same value.

    Parameters
    ----------
    x: numpy.array
      The values to be converted to weights.
    x_curves: tuple
      The values indicating where the low/upper curves should start.

    Returns
    -------
    r : numpy.array
      The weights.
    """
    # Where the two curves should start.
    cmin, cmax = x_curves if x_curves is not None else [np.min(x), np.max(x)]
    # Sigmoid variables.
    z = (x-cmin) / (cmax-cmin)
    # Approximated sigmoid.
    r = (lambda t: (1+self.r**(-t+self.g))**(-1)) (z)
    # Normalize so it goes between zero and one.
    # This happens when cmin=np.min(x) and cmax=n.max(x)
    r = (r-np.min(r)) / (np.max(r)-np.min(r))
    # Return
    return r

  # ---------------------------------------------------------------------------
  #                            HELPER METHODS
  # ---------------------------------------------------------------------------
  def threshold(self, r, x, thresholds=(None,None)):
    """This function thresholds the r given the values of x.

    Parameters
    ----------
    x: numpy.array
      The values to be converted to weights.
    r: numpy.array
      The weights to be thresholded.
    threshold_low: number;
      The values in x lower will have minimum weight.
    treshold_high: number;
      The values in x higher will have maximum weight.

    Returns
    -------
    """
    # Get thresholds
    threshold_low, threshold_high = thresholds

    # Lower threshold.
    if threshold_low is not None: 
      r = np.where(x<threshold_low, 0, r)

    # Upper threshold.
    if threshold_high is not None: 
      r = np.where(x>threshold_high, np.max(r), r)

    # Return
    return r


  # ---------------------------------------------------------------------------
  #                                WEIGHTS
  # ---------------------------------------------------------------------------
  def weights_standard(self, x):
    """This function returns the weights."""
    return self.approximated_sigmoid(x)


  def weights_percentile(self, x, percentiles):
    """This function returns the weights.

    Parameters
    ----------
    x             :
    x_percentiles :

    Returns
    -------
    weights :
    """
    # Get percentiles
    percentile_low, percentile_high = percentiles
    # Create sigmoid with curves in such percentiles.
    r = self.approximated_sigmoid(x, [np.percentile(x, percentile_low), \
                                      np.percentile(x, percentile_high)])
    # Return
    return r


  def weights(self, x):
    """This cuntion computes the weights.

    Parameters
    ----------
    x :
    x_percentiles    :
    x_threshold_low  :
    x_threshold_high :

    Returns
    -------
    """
    # Get the standard sigmoid or a perso
    if self.percentiles is None:
      r = self.weights_standard(x)
    else :
      r = self.weights_percentile(x, self.percentiles)

    # Treshold the result.
    if self.thresholds is not None:
      r = self.threshold(r, x, self.thresholds)

    # Return
    return self.offset + self.scale*r







if __name__ == '__main__': # pragma: no cover

  # Libraries
  import matplotlib as mpl
  import matplotlib.pyplot as plt
  import statsmodels.robust.norms as norms


  # ------------
  # Basic sample
  # ------------
  # Create SigmoidA instance
  W = SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0)

  # Compute weights
  w = np.ones((1, 5)) * 3
  r = W.weights(w)

  # Show
  print("\nWeights:")
  print(w)
  print(r)

  # ----------------
  # Various samples
  # ----------------

  # Matplotlib options
  mpl.rc('legend', fontsize=6)
  mpl.rc('xtick', labelsize=6)
  mpl.rc('ytick', labelsize=6)
  mpl.rc('font', size=7)

  # Set pandas configuration.
  pd.set_option('display.max_colwidth', 14)
  pd.set_option('display.width', 150)
  pd.set_option('display.precision', 4)

  # Constants
  length = 100

  # Create time-series.
  x = np.linspace(0,100,100)
  f = np.concatenate((np.random.rand(35)*50+50,
                      np.random.rand(30)*50+100,
                      np.random.rand(35)*50+150))

  # Weight Functions
  w_functions = [
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[10,90]),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[25,75]),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, percentiles=[40,50]),
    SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0, thresholds=[15,85])]

  # Create figure
  fig, axes = plt.subplots(1,3, figsize=(10,4))

  # Plot frequencies
  axes[1].bar(x, f, color='gray', alpha=0.7, label='Frequency')

  # Plot weights
  for i,W in enumerate(w_functions):
    axes[0].plot(x, W.weights(x), label=W._identifier(short=True))
    axes[2].plot(x, W.weights(f), marker='o', alpha=0.5, 
      markeredgecolor='k', markeredgewidth=0.5, markersize=4, 
      linewidth=0.00, label=W._identifier(short=True))

  # Titles
  axes[0].set_title('Sigmoid Function')
  axes[1].set_title('Frequencies')
  axes[2].set_title('Weights')

  # Legends
  axes[0].legend()
  axes[1].legend()
  axes[2].legend()

  # Tight layout
  plt.tight_layout()

  # Show
  # plt.show()