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
import warnings
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Libraries.
from operator import attrgetter

from statsmodels.tsa.statespace.sarimax import SARIMAX

# Libraries wrapper.
from pyamr.core.regression.wreg import RegressionWrapper


# --------------------------------------------------------------------------
#                              helper methods
# -------------------------------------------------------------------------- 
def _cast_float(e):
    """Casts an element to float when feasible.
    """
    try:
        return float(e)
    except:
        return e


class SARIMAXWrapper(RegressionWrapper):
    """Description

    """

    # --------------------------------------------------------------------------
    #                              overriden
    # --------------------------------------------------------------------------
    def _identifier(self):
        """This method returns the name to idenfy the model.
        """
        return "%s%sx%s [%s,%s]" % (getattr(self, '_name', None),
                                    getattr(self, 'order', None),
                                    getattr(self, 'seasonal_order', '(None)'),
                                    getattr(self, 'trend', None),
                                    getattr(self, 'exog', None) is not None)

    # --------------------------------------------------------------------------
    #                        parameters from summary
    # --------------------------------------------------------------------------
    def _params_from_summary(self):
        """This method returns a dictionariy with the parameters from summary.
        """
        # Format summary
        summary = self._raw.summary().as_csv()
        summary = summary.split("\n", 1)[1]  # Remove first line.
        summary = summary.replace("\n", ",")  # Replace \n by comma.

        # Split in elements.
        elements = summary.split(",")
        elements = [_cast_float(e.strip()) for e in elements]

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
        """This method creates a dictioanry with the relevant parameters.

        @see: statsmodels.Sarimax
        @see: statsmodels.SarimaxResults

        Parameters
        ----------
        alpha : significance level

        Returns
        -------
        dictionary : dictionary with the parameters.
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
                          self._raw.zvalues,
                          self._raw.pvalues,
                          self._raw.conf_int(alpha))

        # Add coefficients statistics to series.
        for name, coef, std, tvalue, pvalue, (cil, ciu) in params_data:
            d['%s_%s' % (name, 'coef')] = coef
            d['%s_%s' % (name, 'std')] = std
            d['%s_%s' % (name, 'tvalue')] = tvalue
            d['%s_%s' % (name, 'tprob')] = pvalue
            d['%s_%s' % (name, 'cil')] = cil
            d['%s_%s' % (name, 'ciu')] = ciu

        # Further statistics.
        d.update(self._params_from_summary())
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
        # Elements to split by.
        find = "=" * 78

        # Split and fill.
        smry = find.join(self._raw.summary(**kwargs).as_text().split(find)[:-1])
        smry = smry.split("\n")
        smry[-6] = smry[-6].replace('=', '', 5)
        smry[-5:] = [v.replace(' ', '', 5) for v in smry[-5:]]
        smry = "\n".join(smry[:-1])

        # Variables.
        om, omp, dw = 0.0, 0.0, self.m_dw
        jb, jbp = self.m_jb_value, self.m_jb_prob
        nm, nmp = self.m_nm_value, self.m_nm_prob
        skew, kurt = self.m_skew, self.m_kurtosis

        # Add in new lines.
        smry += "\n%s\n%s\n%s\n" % ("=" * 78, "Manual".center(78, ' '), "-" * 78)
        smry += "Omnibus:    %#25.3f   Durbin-Watson: %#23.3f\n" % (om, dw)
        smry += "Normal (N): %#25.3f   Prob(N):       %#23.3f\n" % (nm, nmp)
        smry += "=" * 78 + "\n"
        smry += "Note that JB, P(JB), skew and kurtosis have different values.\n"
        smry += "Note that Prob(Q) tests no correlation of residuals."

        # Return
        return smry

    # ---------------------------------------------------------------------------
    #                           prediction method
    # ---------------------------------------------------------------------------
    def get_prediction(self, start=None, end=None, alpha=0.05, **kwargs):
        """This method calls the get prediction function in ARIMA.

        Parameters
        ----------
        start : int (optional)
          The time t to start the prediction

        end : int (optional)
          The time t to end the prediction

        dynamic : bool
          The dynamic keyword affects in-sample prediction. If dynamic is false
          then the in-sample lagged values are used for prediction. if dynamic
          is true, then in-sample forecasts are used in place of lagged dependent
          variables. The first forecasted value is start.

        alpha : float
          The alpha value when creating the norm point percent function to
          compute the confidence intervals for the forecast predictions.

        typ: string-like, options = {linear, levels}
          Wether to predict the original levels (levels) or predict in terms of
          the differenced endogenous variables.

        Returns
        -------
        matrix :
        """
        # Predict levels by default in differenced timeseries.
        if hasattr(self._raw.model, 'k_diff'):
            # Return original levels
            if not 'typ' in kwargs:
                kwargs['typ'] = 'levels'

        # Compute prediction.
        prediction = self._raw.get_prediction(start=start, end=end, **kwargs)

        # Compute time.
        time = self._time(start=start, end=end)

        # Divide predictions in insample/forecast
        pred_in = prediction.predicted_mean[time < len(self.endog)]

        # Get plotting values.
        mean = prediction.predicted_mean
        cito = prediction.conf_int()  # .as_matrix()

        # Add the insample confidence interval. Note that the prediction
        # conf_int implemented above computes the forecast error. However,
        # there are some observatons (pred_in) which have been seen during
        # model fitting and therefure they are not pure forecasts.
        cito[:len(pred_in), :] = self.conf_int_insample(pred_in, alpha=alpha)

        # Get plotting values.
        return np.column_stack((time, mean, cito)).T

    # --------------------------------------------------------------------------
    #                           auto method
    # --------------------------------------------------------------------------
    def auto(self, endog, exog=None, ic='bic', max_ar=3, max_ma=3, max_d=1,
             max_P=0, max_D=0, max_Q=0, list_s=[12], warn='ignore',
             trends=['n', 'c', 't', 'ct'], return_fits=False, verbose=0,
             converged=True, **kwargs):
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

        max_P : number

        max_D : number

        max_Q : number

        list_s : array-like

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
        orders = list(itertools.product(*[np.arange(0, max_ar + 1),
                                          np.arange(0, max_d + 1),
                                          np.arange(0, max_ma + 1)]))

        # Similar than previous guide but with seasonal orders.
        seasonal_orders = list(itertools.product(*[np.arange(0, max_P + 1),
                                                   np.arange(0, max_D + 1),
                                                   np.arange(0, max_Q + 1),
                                                   list_s]))

        # Parameters
        grid_params = {'exog': [exog],
                       'endog': [endog],
                       'order': orders,
                       'seasonal_order': seasonal_orders,
                       'trend': trends,
                       'disp': [0]}

        # Perform grid search
        with warnings.catch_warnings():
            # What to do with the warnings
            warnings.filterwarnings(warn)
            # Perform grid search.
            wrappers = self.grid_search(grid_params=grid_params, verbose=verbose)

        # Keep only those that converged.
        if converged:
            wrappers = [w for w in wrappers if w.converged]

        # Return all
        if return_fits:
            return wrappers, min(wrappers, key=attrgetter(ic))

        # Return best
        return min(wrappers, key=attrgetter(ic))

    # ---------------------------------------------------------------------------
    #                             OTHER METHODS
    # ---------------------------------------------------------------------------
    def save(self, **kwargs):
        """This method saves the information.
        """
        self._raw.save(**kwargs)

    def load(self, **kwargs):
        """This method loads the information.
        """
        # Load.
        self._raw = sm.load(**kwargs)
        self._resid = self._raw.resid
        self._result = self._init_result()
        self._config = self._init_config()
        # Return.
        return self


if __name__ == '__main__':

    # Import
    import sys
    import warnings
    import pandas as pd
    import matplotlib as mpl
    import matplotlib.pyplot as plt

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

    # ----------------------------
    # fit the model
    # ----------------------------
    # Create specific sarimax model.
    sarimax = SARIMAXWrapper(SARIMAX).fit(endog=y[:80],
                                          exog=None,
                                          trend='ct',
                                          seasonal_order=(1, 0, 1, 12),
                                          order=(0, 1, 1),
                                          disp=0)

    # Print series.
    print("\nSeries:")
    print(sarimax.as_series())

    # Print summary.
    print("\nSummary:")
    print(sarimax.as_summary())

    # -----------------
    # Save & Load
    # -----------------
    # File location
    # fname = '../../examples/saved/sarimax-sample.pickle'

    # Save
    # sarimax.save(fname=fname)

    # Load
    # sarimax = SARIMAXWrapper().load(fname=fname)

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
    preds_1 = sarimax.get_prediction(start=s, end=e, dynamic=False)
    preds_2 = sarimax.get_prediction(start=s, end=e, dynamic=True)

    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(8, 3))

    # Plot non-dynamic
    # ----------------
    # Plot truth values.
    axes[0].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=5, linewidth=0.75, label='Observed')

    # Plot forecasted values.
    axes[0].plot(preds_1[0, :], preds_1[1, :], color='#FF0000', alpha=1.00,
                 linewidth=2.0, label=sarimax._identifier())

    # Plot the confidence intervals.
    axes[0].fill_between(preds_1[0, :], preds_1[2, :],
                         preds_1[3, :],
                         color='#FF0000',
                         alpha=0.25)

    # Plot dynamic
    # ------------
    # Plot truth values.
    axes[1].plot(y, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=5, linewidth=0.75, label='Observed')

    # Plot forecasted values.
    axes[1].plot(preds_2[0, :], preds_2[1, :], color='#FF0000', alpha=1.00,
                 linewidth=2.0, label=sarimax._identifier())

    # Plot the confidence intervals.
    axes[1].fill_between(preds_2[0, :], preds_2[2, :],
                         preds_2[3, :],
                         color='#FF0000',
                         alpha=0.25)

    # Configure axes
    axes[0].set_title("SARIMAX non-dynamic")
    axes[1].set_title("SARIMAX dynamic")

    # Format axes
    axes[0].grid(True, linestyle='--', linewidth=0.25)
    axes[1].grid(True, linestyle='--', linewidth=0.25)

    # Legend
    axes[0].legend()
    axes[1].legend()

    plt.show()

    # -------------------------------
    # Example II - AUTO
    # -------------------------------
    # This example shows how to use auto to find the best overall model using
    # a particular seletion criteria. It also demonstrates how to plot the
    # resulting data for visualization purposes. Note that it only prints
    # the top best classifier according to the information criteria.
    #
    # To do: Review the dynamic=True.

    sarimax = SARIMAXWrapper(estimator=SARIMAX)

    # Find the best arima model (bruteforce).
    models, best = sarimax.auto(endog=y[:80], ic='bic',
                                max_ar=2,
                                max_ma=3,
                                max_d=1,
                                max_P=1,
                                max_D=0,
                                max_Q=1,
                                list_s=[1],
                                verbose=1,
                                return_fits=True)

    # Sort the list (from lower to upper)
    models.sort(key=lambda x: x.bic, reverse=False)

    # Summary
    summary = sarimax.from_list_dataframe(models)

    # Show summary
    print("\nSummary:")
    print(summary[['sarimax-order',
                   'sarimax-seasonal_order',
                   'sarimax-trend',
                   'sarimax-aic',
                   'sarimax-bic']])

    # Create figure
    fig, axes = plt.subplots(3, 3, figsize=(10, 6))
    axes = axes.flatten()

    # Loop for the selected models
    for i, estimator in enumerate(models[:9]):
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
        axes[i].plot(preds[0, :], preds[1, :], color='#FF0000', alpha=1.00,
                     linewidth=2.0, label=estimator._identifier())

        # Plot the confidence intervals.
        axes[i].fill_between(preds[0, :], preds[2, :],
                             preds[3, :],
                             color='#FF0000',
                             alpha=0.25)

        # Configure axes
        axes[i].legend(loc=3)
        axes[i].grid(True, linestyle='--', linewidth=0.25)

    # Set superior title
    plt.suptitle("Dynamic predictions for SARIMAX")

    # Show
    plt.show()
