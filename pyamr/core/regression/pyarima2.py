##############################################################################
# Author: Bernard Hernandez
# Filename: 03-main-create-sari-idxs.py
#
# Description : This file contains differnent statistics used in time-series.
#               What it mainly does is to format the output of tests provided
#               by external libraries and return them in a dataframe.
#
#
###############################################################################
# Forces decimals on divisions.
from __future__ import division 

# Libraries
import sys
import math
import inspect
import warnings
import itertools
import numpy as np
import pandas as pd

# Libraries.
from scipy.stats import norm
from operator import attrgetter

# Import pyramid arima
from pyramid.arima import ARIMA as PYARIMA

# Add module wrappers to sys path dynamically.
sys.path.append("../../../")

# Libraries wrapper.
from pyAMR.core.regression.wreg import RegressionWrapper
from pyAMR.core.stats.wbase import getargspecdict

class PyramidWrapper(RegressionWrapper):


  def _identifier(self):
    """This method creates a name that describes de model."""
    try:    exogenous = self.exogenous is not None
    except: exogenous = False

    return "%s%sx%s [%s,%s]" % (self._name,
                                self.order,
                                self.seasonal_order,
                                self.trend,
                                exogenous) 

  # --------------------------------------------------------------------------
  #                           SET VARIABLES
  # --------------------------------------------------------------------------
  def _params_from_summary(self):
    """Gets parameters from the summary result of the raw object.
    """
    # Format summary
    summary = self._raw.summary().as_csv()
    summary = summary.split("\n",1)[1]     # Remove first line.
    summary = summary.replace("\n",",")    # Replace \n by comma.

    # Split in elements.
    elements = summary.split(",")
    elements = [self._cast_float(e.strip()) for e in elements]

    # Create series.
    d = {}

    # Add parameters.
    d['s_jb_value'] = elements[-13]
    d['s_jb_prob'] = elements[-9]
    d['s_skew'] = elements[-5]
    d['s_Q_value'] = elements[-15]
    d['s_Q_prob'] = elements[-11]
    d['s_H_value'] = elements[-7]
    d['s_H_prob'] = elements[-3]
    d['s_kurtosis'] = elements[-1]
    d['s_heteroskedasticity'] = elements[-7]
    d['s_omnibus_value'] = None
    d['s_omnibus_prob'] = None

    # Return
    return d

  def evaluate(self, alpha=0.05):
    """This method set all the variables into this class.

    @see: statsmodels.Arima
    @see: statsmodels.ArimaResults

    Parameters
    ---------- 
    alpha :

    Returns
    -------
    series :
    """
    # Create series.
    d = {}
    
    # Add generic metrics.
    d['aic'] = self._raw.aic()
    d['aicc'] = self._raw.aicc()
    d['bic'] = self._raw.bic()
    d['hqic'] = self._raw.hqic()
    d['llf'] = self._raw.arima_res_.llf

    # Check if it is arima or sarimax and get corresponding values
    if self._raw.seasonal_order is not None:
      statistic_values = self._raw.arima_res_.zvalues
    else:
      statistic_values = self._raw.arima_res_.tvalues,

    # Create params information.
    params_data = zip(self._raw.arima_res_.data.param_names,
                      self._raw.arima_res_.params,
                      self._raw.arima_res_.bse,
                      statistic_values,
                      self._raw.arima_res_.pvalues,
                      self._raw.arima_res_.conf_int(alpha))

    # Add coefficients statistics to series.
    for name, coef, std, tvalue, pvalue, (cil, ciu) in params_data:
      d['%s_%s'%(name, 'coef')] = coef
      d['%s_%s'%(name, 'std')] = std
      d['%s_%s'%(name, 'tvalue')] = tvalue
      d['%s_%s'%(name, 'tprob')] = pvalue
      d['%s_%s'%(name, 'cil')] = cil
      d['%s_%s'%(name, 'ciu')] = ciu

    # Further statistics
    d.update(self._resid_stats())

    # We cannot use the params_from_summary because this wrappers stores 
    # different models with different summaries. The right way to solve this
    # is by performing the statistics related with the residuals in the
    # regression_wrapper._resid_stats.
    #d.update(self._params_from_summary())

    # Return
    return d

  def _init_config(self):
    """This method initialises the configuration.

    For some reason the interestin data is in the method __init__ for the
    object self._raw (ARIMA) and the method fir for the object
    self._raw.arima_res_.model.

    TODO: Handle if the instances passed to getargspecdict do not exist.
    """
    # Create dictionary.
    d = {}

    # Fill it.
    d.update(self._getargspecdict(self._raw.arima_res_.model, 'fit'))
    d.update(self._getargspecdict(self._raw, '__init__'))

    # Return
    return d

  # --------------------------------------------------------------------------
  #                           HELPER METHODS
  # --------------------------------------------------------------------------
  def as_summary(self, **kwargs):
    """This method displays the summary.
    """ 
    # Elements to split by.
    find = "="*78
    # Split and fill.
    smry = find.join(self._raw.summary(**kwargs).as_text().split(find)[:-1])
    smry = smry.split("\n")
    smry[-6] = smry[-6].replace('=','',5)
    smry[-5:] = [v.replace(' ', '', 5) for v in smry[-5:]]
    smry = "\n".join(smry[:-1])
    # Variables.
    om, omp, dw = 0.0, 0.0, self.m_dw
    jb, jbp = self.m_jb_value, self.m_jb_prob
    nm, nmp = self.m_nm_value, self.m_nm_prob
    skew, kurt = self.m_skew, self.m_kurtosis
    # Add in new lines.
    smry+= "\n%s\n%s\n%s\n" % ("="*78, "Manual".center(78, ' '), "-"*78)
    smry+= "Omnibus:    %#25.3f   Durbin-Watson: %#23.3f\n" % (om, dw)
    smry+= "Normal (N): %#25.3f   Prob(N):       %#23.3f\n" % (nm, nmp) 
    smry+= "="*78 + "\n"
    smry+= "Note that JB, P(JB), skew and kurtosis have different values.\n"
    smry+= "Note that Prob(Q) tests no correlation of residuals."
    # Return
    return smry
    
  # --------------------------------------------------------------------------
  #                                 FIT
  # --------------------------------------------------------------------------
  def resid(self):
    """Get the residual"""
    return self._raw.resid()



  # ---------------------------------------------------------------------------
  #                               PREDICTION
  # ---------------------------------------------------------------------------
  def get_prediction(self, start=None, end=None, alpha=0.05, **kwargs):
    """
    """
    # Compute time
    time = self._time(start=start, end=end)

    # Compute prediction
    mean = self._raw.predict_in_sample(start=start, end=end, **kwargs)

    # Confidence interval
    cito = self.conf_int_insample(mean, alpha=0.05)

    # For some reason the predict_in_sample function implemented in the
    # module pyramid-arima returns more samples than it should. Moreover
    # although there is another method call predict for forecasting, the
    # predict in sample functions seems to do both. Thus such function
    # is used and the first end-start elemnts are kept. A
    mean = mean[:time.size]
    cito = cito[:time.size]
    
    # Return
    return np.column_stack((time, mean, cito)).T


  # ---------------------------------------------------------------------------
  #                               FIND AUTO
  # ---------------------------------------------------------------------------
  def from_instance(self, arima, **kwargs):
    """This method constructs a PyramidWrapper object from pyramid.ARIMA
    """
    # Create object.
    instance = PyramidWrapper()
    # Set model.
    instance._raw = arima
    # Set residuals as attribute.
    instance._resid = arima.resid()
    # Set series with interesting params.
    instance._result = instance.evaluate(alpha=0.05)

    # Find arima configuration parameters
    d = {}
    d.update(getargspecdict(arima.arima_res_.model, 'fit'))
    d.update(getargspecdict(arima, '__init__'))

    # Set configuration parameters
    instance._config = instance._init_config()

    # Return
    return instance


  def auto(self, **kwargs):
    """This method finds the best arima.

    @see pyrmid.arima.auto_arima

    Parameters
    ----------

    Returns
    -------
    """
    # Library.
    from pyramid.arima import auto_arima
    from pyramid.arima.arima import ARIMA

    # Compute auto_arima.
    results = auto_arima(**kwargs)

    # Return a single PyramidWrapper object.
    if isinstance(results, ARIMA):
      return [self.from_instance(results)]

    # Return an array of PyramidWrapper objects.
    if isinstance(results, list):
      return [PyramidWrapper().from_instance(a) for a in results]








if __name__ == '__main__':

  # Libraries.
  import matplotlib.pyplot as plt

  # Set pandas configuration.
  pd.set_option('display.max_colwidth', 14)
  pd.set_option('display.width', 80)
  pd.set_option('display.precision', 4)

  # Constants
  length = 100
  offset = 100
  slope = 10

  # Create time-series.
  x = np.arange(length)
  n = np.random.randn(length)*150
  y = slope*x + offset + n

  # Format exog to be used in pyramid-arima.
  exog = x.reshape(-1,1)

  # Create object
  # This is a wrapper for the methods arima and sarimax within statstools. Take
  # to account the following things when using this wrapper:
  # - seasonal_order = None calls arima, otherwise it calls sarimax.
  # - transparams = True enforces stationarity (not sure).
  # - the exogenous variable needs to be reshaped.
  # - the trend is passed in the constructor (insted of the fit method).
  pyramid = PyramidWrapper(estimator=PYARIMA).fit(y=y[:80], 
                exogenous=None, order=(2,1,2), seasonal_order=(0,0,0,0),
                trend='c', disp=0)

  # Print series.
  print pyramid.as_series()

  # Print summary.
  print pyramid.as_summary()

  # -----------------
  # Save & Load
  # -----------------
  # TODO: There is a TypeError: can't pickle zStatespace objects when the
  #       seasonal order is included in the PyramidWrapper. However, 
  #       apparently we are able to save sarimax with seasons using the
  #       SARIMAXWrapper.
  # File location
  #fname = '../../examples/saved/pyramid-sample.pickle'

  # Save
  #pyramid.save(fname=fname)

  # Load
  #pyramid = PyramidWrapper().load(fname=fname)


  # -----------------
  #  Predictions
  # -----------------
  # Variables.
  s, e, d = 50, 120, False

  # Compute predictions (exogenous?).
  preds = pyramid.get_prediction(start=s, end=e, dynamic=d, exogenous=None)

  # Plot truth values.
  plt.plot(y, color='#A6CEE3', alpha=0.5, marker='o',
              markeredgecolor='k', markeredgewidth=0.5,
              markersize=5, linewidth=0.75, label='Observed')

  # Plot forecasted values.
  plt.plot(preds[0,:], preds[1,:], color='#FF0000', alpha=1.00, 
              linewidth=2.0, label=pyramid._identifier())

  # Plot the confidence intervals.
  plt.fill_between(preds[0,:], preds[2,:], 
                               preds[3,:], 
                               color='r', 
                               alpha=0.1)
          
  # Legend 
  plt.legend()

  plt.show()


  # -------------------
  #   Grid search
  # -------------------
  # Grid parameters.
  fit_params = {'exogenous': [None, exog],
                'y': [y], 'disp': [0], 
                'order': [(0,1,1)], 
                'seasonal_order': [None],
                'trend': ['n','c','t','ct']}

  # Get summary.
  models = pyramid.grid_search(grid_params=fit_params)

  # Summary
  summary = pyramid.from_list_dataframe(models).T

  # Plot result.
  print "\nSummary"
  print summary

  # -------------------
  # autoarima
  # -------------------

  # Example 1: Retrieving just the best fit.
  # ----------------------------------------
  # Find best arima fit.
  stepwise_fit = PyramidWrapper().auto(y=y, trend='c', 
    exogenous=None, 
    start_p=0, start_q=0, max_p=0, max_q=5, d=0,
    seasonal=False, start_P=0, D=1, 
    trace=True,
    error_action='ignore',       # ignore if an order does not work.
    suppress_warnings=True,      # ignore convergence warnings.
    information_criterion='bic', # score to select best model.
    return_valid_fits=False,      # Return all valid fits.
    stepwise=True)               # set to stepwise

  # Get summary.
  summary = PyramidWrapper().from_list_dataframe(stepwise_fit, flabel=False).T

  # -----------------
  #  Predictions
  # -----------------
  # Variables.
  s, e, d = 50, 120, False

  # Compute predictions (exogenous?).
  preds = stepwise_fit[0].get_prediction(start=s, end=e, dynamic=d, exogenous=None)

  # Plot truth values.
  plt.plot(y, color='#A6CEE3', alpha=0.5, marker='o',
              markeredgecolor='k', markeredgewidth=0.5,
              markersize=5, linewidth=0.75, label='Observed')

  # Plot forecasted values.
  plt.plot(preds[0,:], preds[1,:], color='#FF0000', alpha=1.00, 
              linewidth=2.0, label=pyramid._identifier())

  # Plot the confidence intervals.
  plt.fill_between(preds[0,:], preds[2,:], 
                               preds[3,:], 
                               color='r', 
                               alpha=0.1)
          
  # Legend 
  plt.legend()

  plt.show()

  # Print result.
  print "\nAuto Stepwise Summary"
  print summary


  # Retrieving all fits
  # -------------------
  # Do a grid search using auto_arima.
  brute_fit = PyramidWrapper().auto(y=y, 
    exogenous=None, trend='c',
    start_p=0, d=1, start_q=0, max_p=0, max_d=1, max_q=5, 
    start_P=1, D=None, start_Q=1, max_P=2, max_D=1, max_Q=2, 
    max_order=20, m=1, seasonal=False, stationary=False, 
    information_criterion='bic', alpha=0.05, stepwise=False, 
    return_valid_fits=True,
    test='kpss', seasonal_test='ch', n_jobs=1, start_params=None, method=None, 
    transparams=True, solver='lbfgs', maxiter=50, disp=0, callback=None,
    offset_test_args=None, seasonal_test_args=None, suppress_warnings=False, 
    error_action='ignore', trace=False, random=False, random_state=None, 
    n_fits=None, out_of_sample_size=0, scoring='mse', scoring_args=None)
 

  print len(brute_fit)
  # Create summary dataframe
  summary = PyramidWrapper().from_list_dataframe(brute_fit, flabel=False).T

  # Plot result.
  print "\nAuto Brute Force Summary"
  print summary

  # Show.
  plt.show()