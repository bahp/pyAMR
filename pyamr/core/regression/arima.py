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

# Import ARIMA from statsmodels.
from statsmodels.tsa.arima_model import ARIMA

# Libraries wrapper.
from pyamr.core.regression.wreg import RegressionWrapper
from pyamr.core.regression.wreg import _forecast_error
from pyamr.core.regression.wreg import _forecast_conf_int
from pyamr.core.regression.wreg import _insample_conf_int


class ARIMAWrapper(RegressionWrapper):
  """Description


  """

  # --------------------------------------------------------------------------
  #                              overriden
  # --------------------------------------------------------------------------
  def _identifier(self):
    """The name to identify the arima model."""
    return "%s%s [%s, %s]" % (getattr(self, '_name', None),
                              getattr(self, 'order', None),
                              getattr(self, 'trend', None),
                              getattr(self, 'exog', None) is not None)

  # --------------------------------------------------------------------------
  #                         confidence intervals
  # --------------------------------------------------------------------------
  def conf_int_forecast(self, predictions, alpha=0.05):
    """Computes the out-sample confidence interval.

    Parameters
    ----------
    predictions : array-like
      The predictions done by the model.

    alpha : int
      The alpha to configure the confidence interval.

    Returns
    -------
    array-like
    """
    # Compute forecast error
    fcasterr = _forecast_error(sigma2=self._raw.sigma2, 
                               arparams=self._raw.arparams, 
                               maparams=self._raw.maparams,
                               steps=predictions.shape[0])
    # Compute forecast interval
    ciou = _forecast_conf_int(forecast=predictions, 
                              fcasterr=fcasterr, 
                              alpha=alpha)
    # Return
    return ciou


  # --------------------------------------------------------------------------
  #                              evaluate
  # --------------------------------------------------------------------------
  def evaluate(self, alpha=0.05):
    """This method creates a dictionary with the relevant attributes.

    .. note:: 
          
          There is an issue with the method conf_int(alpha). It can receive 
          as input parameters a pandas series or a numpy array. We are using 
          it with numpy array as input, hence when pandas series is passed 
          the method _init_result gives an error.

    @see: statsmodels.Arima
    @see: statsmodels.ArimaResults

    Parameters
    ---------- 
    alpha : the confidence interval.

    Returns
    -------
    dictionary : map with all the parameters.
    """
    # Create series.
    d = {} 

    # Add generic metrics.
    d['aic'] = self._raw.aic
    d['bic'] = self._raw.bic
    d['hqic'] = self._raw.hqic
    d['llf'] = self._raw.llf

    # Create params information.
    params_data = zip(self._raw.data.param_names,
                      self._raw.params,
                      self._raw.bse,
                      self._raw.tvalues,
                      self._raw.pvalues,
                      self._raw.conf_int(alpha))

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

    # Extra useful infomation
    d['converged'] = self._raw.mle_retvals['converged']

    # Return
    return d

  # --------------------------------------------------------------------------
  #                             summary method
  # --------------------------------------------------------------------------
  def as_summary(self, **kwargs):
    """This method creates a summary string.
    """ 
    # Variables.
    n = 12 + len(self._raw.params)
    om, omp , dw = 0.0, 0.0, self.m_dw
    jb, jbp = self.m_jb_value, self.m_jb_prob
    nm, nmp = self.m_nm_value, self.m_nm_prob
    skew, kurt = self.m_skew, self.m_kurtosis

    # Summary.
    smry = "\n".join(self._raw.summary(**kwargs).as_text().split("\n")[:n])
    
    # Add in new lines.
    smry+= "\n%s\n%s\n%s\n" % ("="*78, "Manual".center(78, ' '), "-"*78)
    smry+= "Omnibus:       %#22.3f  Durbin-Watson:    %#21.3f\n" % (om, dw)
    smry+= "Prob(Omnibus): %#22.3f  Jarque-Bera (JB): %#21.3f\n" % (omp, jb)
    smry+= "Skew:          %#22.3f  Prob(JB):         %#21.3f\n" % (skew, jbp)
    smry+= "Kurtosis_m:    %#22.3f  Cond No:                 \n" % (kurt) 
    smry+= "Normal (N):    %#22.3f  Prob(N):          %#21.3f\n" % (nm, nmp) 
    smry+= "="*78

    # Return
    return smry
  
  # ---------------------------------------------------------------------------
  #                             prediction method
  # ---------------------------------------------------------------------------
  def get_prediction(self, start=None, end=None, alpha=0.05, **kwargs):
    """This method calls the predict function in ARIMA.

    .. note:: 

      The confidence intervals have been implemented using the functions
      ``_forecast_conf_int()`` and ``_forecast_error()`` implemented in the 
      statsmodels.ts.arima_model.ARIMAResults. As such, it produces the 
      same confidence intervals than the method ``plot_predict()``.

    .. note:: 
    
      The parameter start refers to the original series. As such, if the 
      series has been differenced (e.g. d=1) the first observation has 
      been lost. In those cases, start has to be greater or equal to d.

    .. todo::

      - Review the predictions when dynamic is set to true. 
      - Review the confidence intervals (in and out sample)
      - Review the prediction intervals.

    Parameters
    ----------
    start : int (optional)
      The time t to start the prediction

    end : int (optional)
      The time t to end the prediction

    dynamic : bool
      The dynamic keyword affects in-sample prediction. If dynamic is false
      then the in-sample lagged values are used for prediction. if dynamic
      is true, then in-sample forecasts are used in place of lagged 
      dependent variables. The first forecasted value is start.

    alpha: float
      The alpha value when creating the norm point percent function to
      compute the confidence intervals for the forecast predictions.

    typ: string-like, options = {linear, levels}
      Wether to predict the original levels (levels) or predict in terms of 
      the differenced endogenous variables.

    Returns
    -------
    matrix : 
    """
    # The series has been differenced.
    if hasattr(self._raw.model, 'k_diff'):
      # Return original levels.
      if not 'typ' in kwargs:
        kwargs['typ'] = 'levels' 

    # Compute prediction
    pred = self._raw.predict(start=start, end=end, **kwargs)

    # Compute time.
    time = self._time(start=start, end=end)

    # Divide predictions in insample/forecast
    pred_in = pred[time<len(self.endog)]
    pred_ou = pred[time>=len(self.endog)]

    # Compute confidence intervals
    ciin = self.conf_int_insample(pred_in, alpha=alpha) 
    ciou = self.conf_int_forecast(pred_ou, alpha=alpha)
    cito = np.concatenate((ciin, ciou))

    # Get plotting values.
    return np.column_stack((time, pred, cito)).T


  # ---------------------------------------------------------------------------
  #                               auto method
  # ---------------------------------------------------------------------------
  def auto(self, endog, exog=None, ic='bic', trends=['nc','c'], max_ar=3, 
                 max_ma=3, max_d=1, warn='ignore', return_fits=False, 
                 converged=True, disp=0, verbose=0, **kwargs):
    """This method finds the best arima through bruteforce.

    Note: It uses grid search through the base wrapper.

    Parameters
    ----------
    endog : array-like
      The endogenous variable (aka. time series data)

    exog : array-like
      The exogenous variable (by default is the time t starting in 0)

    ic : string
      The information criteria which should be any of the params which
      are set in the wrapper (see method _init_result).

    max_ar : number
      The maximum autorregresive order to inspect.

    max_ma : number
      The maximum moving average order to inspect.

    max_d : number
      The maximum difference to inspect.

    warn : string, options = {ignore, raise}
      Whether or not to ignore the warnings raised

    return_fits: bool
      Whether or not to return all the fits. If false only the best model 
      is returned. If true all the models and the best model are returned
      separately.

    converged: bool
      Whether or not to return only converging models. If false all models
      are returned. If true, only those models that converged are returned.

    Returns
    -------
    """
    # Compute all the orders to perform bruteforce search.
    # Note that some orders are not valid, these will throw an
    # exception that will be catched in the base wrapper 
    # grid_search method. For instance (0,0,0) is invalid.
    orders = set(itertools.product(*[np.arange(0,max_ar+1),
                                     np.arange(0,max_d+1),
                                     np.arange(0,max_ma+1)]))

    # Parameters
    grid_params = {'exog': [exog], 
                   'endog': [endog], 
                   'order': orders,
                   'trend': trends, 
                   'disp': [0]}

    # Perform grid search
    with warnings.catch_warnings():
      # What to do with the warnings
      warnings.filterwarnings(warn)
      # Perform gridsearch.
      wrappers = self.grid_search(grid_params=grid_params, verbose=verbose)

    # Keep only those that converged.
    if converged:
      wrappers = [w for w in wrappers if w.converged]

    # Return all
    if return_fits:
      return wrappers, min(wrappers, key=attrgetter(ic))
    
    # Return only best
    return min(wrappers, key=attrgetter(ic))












if __name__ == '__main__':

  # Import
  import sys
  import warnings
  import pandas as pd
  import matplotlib as mpl
  import matplotlib.pyplot as plt

  # Filter warnings
  warnings.simplefilter(action='ignore', category=FutureWarning)

  # Set pandas configuration.
  pd.set_option('display.max_colwidth', 14)
  pd.set_option('display.width', 140)
  pd.set_option('display.precision', 4)

  # Import own libraries
  from pyamr.datasets.load import make_timeseries

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

  # Create exogenous variable
  exog = x

  # ----------------------------
  # fit the model
  # ----------------------------
  # Create specific arima model.
  arima = ARIMAWrapper(estimator=ARIMA).fit(endog=y[:80], 
                                            order=(1,0,0), 
                                            trend='c', 
                                            disp=0)
  
  # Print series
  print("\nSeries:")
  print(arima.as_series())

  # Print summary.
  print("\nSummary:")
  print(arima.as_summary())

  # -----------------
  # Save & Load
  # -----------------
  # File location
  #fname = '../../examples/saved/arima-sample.pickle'

  # Save
  #arima.save(fname=fname)

  # Load
  #arima = ARIMAWrapper().load(fname=fname)


  # -------------
  #  Example I
  # -------------
  # This example shows how to make predictions using the wrapper which has
  # been previously fitted. It also demonstrateds how to plot the resulting
  # data for visualization purposes. It shows two different types of
  # predictions:
  #    - dynamic predictions in which the prediction is done based on the
  #      previously predicted values. Note that for the case of ARIMA(0,1,1)
  #      it returns a line.
  #    - not dynamic in which the prediction is done based on the real
  #      values of the time series, no matter what the prediction was for
  #      those values.

  # Variables.
  s, e = 50, 120

  # Compute predictions
  preds_1 = arima.get_prediction(start=s, end=e, dynamic=False)
  preds_2 = arima.get_prediction(start=s, end=e, dynamic=True)

  # Create figure
  fig, axes = plt.subplots(1, 2, figsize=(8,3))

  # Plot non-dynamic
  # ----------------
  # Plot truth values.
  axes[0].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                  markeredgecolor='k', markeredgewidth=0.5,
                  markersize=5, linewidth=0.75, label='Observed')

  # Plot forecasted values.
  axes[0].plot(preds_1[0,:], preds_1[1,:], color='#FF0000', alpha=1.00, 
              linewidth=2.0, label=arima._identifier())
  
  # Plot the confidence intervals.
  axes[0].fill_between(preds_1[0,:], preds_1[2,:], 
                                     preds_1[3,:], 
                                     color='#FF0000', 
                                     alpha=0.25)

  # Plot dynamic
  # ------------
  # Plot truth values.
  axes[1].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                  markeredgecolor='k', markeredgewidth=0.5,
                  markersize=5, linewidth=0.75, label='Observed')

  # Plot forecasted values.
  axes[1].plot(preds_2[0,:], preds_2[1,:], color='#FF0000', alpha=1.00, 
              linewidth=2.0, label=arima._identifier())
  
  # Plot the confidence intervals.
  axes[1].fill_between(preds_2[0,:], preds_2[2,:], 
                                     preds_2[3,:], 
                                     color='#FF0000', 
                                     alpha=0.25)

  # Configure axes
  axes[0].set_title("ARIMA non-dynamic")
  axes[1].set_title("ARIMA dynamic")

  # Format axes
  axes[0].grid(True, linestyle='--', linewidth=0.25)
  axes[1].grid(True, linestyle='--', linewidth=0.25)

  # Legend 
  axes[0].legend()
  axes[1].legend()


  # -------------------------------
  # Example II - AUTO
  # -------------------------------
  # This example shows how to use auto to find the best overall model using
  # a particular seletion criteria. It also demonstrates how to plot the 
  # resulting data for visualization purposes. Note that it only prints
  # the top best classifier according to the information criteria.
  #
  # To do: Review the dynamic=True.
  # Create object
  arima = ARIMAWrapper(estimator=ARIMA)

  # Find the best arima model (bruteforce).
  models, best = arima.auto(endog=y[:80], ic='bic', max_ar=3,  
                                                    max_ma=3, 
                                                    max_d=3,
                                                    return_fits=True)

  # Sort the list (from lower to upper)
  models.sort(key=lambda x: x.bic, reverse=False)

  # Summary
  summary = arima.from_list_dataframe(models)

  # Show summary
  print("\nSummary:")
  print(summary[['arima-order',
                 'arima-trend', 
                 'arima-aic', 
                 'arima-bic']])

  # Create figure
  fig, axes = plt.subplots(3,3, figsize=(10,6))
  axes = axes.flatten()

  # Loop for the selected models
  for i,estimator in enumerate(models[:9]):

    # Show information
    print("%2d. Estimator (bic=%.2f): %s " % \
      (i, estimator.bic, estimator._identifier()))

    # Get the predictions
    preds = estimator.get_prediction(start=s, end=e, dynamic=False)

    # Plot truth values.
    axes[i].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                    markeredgecolor='k', markeredgewidth=0.5,
                    markersize=5, linewidth=0.75, label='Observed')

    # Plot forecasted values.
    axes[i].plot(preds[0,:], preds[1,:], color='#FF0000', alpha=1.00, 
                 linewidth=2.0, label=estimator._identifier())
    
    # Plot the confidence intervals.
    axes[i].fill_between(preds[0,:], preds[2,:], 
                                     preds[3,:], 
                                     color='#FF0000', 
                                     alpha=0.25)

    # Configure axes
    axes[i].legend(loc=3)
    axes[i].grid(True, linestyle='--', linewidth=0.25)

  # Set superior title
  plt.suptitle("Dynamic predictions for ARIMA")

  # Show
  plt.show()
