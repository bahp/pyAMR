##############################################################################
# Author: Bernard Hernandez
# Filename: wls.py
#
# Description : This file contains a wrapper for the weighted least squares
#               prediction model implemented in statsmodels.
#
###############################################################################
# Import future
from __future__ import division

# Libraries
import sys
import copy
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Import specific
from statsmodels.sandbox.regression.predstd import wls_prediction_std

# Libraries wrapper.
from pyamr.core.regression.wreg import RegressionWrapper
from pyamr.core.stats.wbase import fargs


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


class PredictionResult():

    def __init__(self, mean, cilo, ciup, pstd, pilo,
                 piup, time, nobs, endog):
        """The constructor

        Parameters
        ----------

        Returns
        -------
        """
        # Set variables
        self.mean = mean
        self.cilo = cilo
        self.ciup = ciup
        self.pstd = pstd
        self.pilo = pilo
        self.piup = piup
        self.time = time
        self.nobs = nobs
        self.endog = endog

        # Set combined interval
        self.bilo, self.biup = np.copy(cilo), np.copy(ciup)
        self.bilo[self.nobs:] = self.pilo[self.nobs:]
        self.biup[self.nobs:] = self.piup[self.nobs:]


class WLSWrapper(RegressionWrapper):
    """The description...

    """

    # Attributes.
    _name = 'WLS'  # Label to add to the attributes when saving.

    # --------------------------------------------------------------------------
    #                           helper methods
    # --------------------------------------------------------------------------
    def _identifier(self, **kwargs):
        """This methods describes de model."""
        # Returns description
        if self.W is not None:
            if hasattr(self.W, '_identifier'):
                return "%s(%s,%s)" % (self._name,
                                      self.trend,
                                      self.W._identifier(**kwargs))
            else:
                return "%s(%s,%s)" % (self._name,
                                      self.trend,
                                      self.W.__class__.__name__)
        # Return basic
        return "%s(%s)" % (self._name, self.trend)

    def pred_int(self, start=None, end=None, **kwargs):
        """This method computes the prediction intervals

        Parameters
        ----------
        start : int (optional)
          The time t to start the prediction

        end : int (optional)
          The time t to end the prediction

        Returns
        -------
        the standard prediction error and the prediction intervals
        """
        # Create the exogenous variable for prediction
        exog = self._exog(start, end)
        # Compute
        pstd, pilo, piup = wls_prediction_std(self._raw, exog=exog, **kwargs)
        # Retrn
        return np.column_stack((pilo, piup))

    # --------------------------------------------------------------------------
    #                            set variables
    # --------------------------------------------------------------------------
    def _params_from_summary(self):
        """Gets parameters from the summary result of the raw object.
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
        d['s_dw'] = elements[-13]
        d['s_jb_value'] = elements[-9]
        d['s_jb_prob'] = elements[-5]
        d['s_skew'] = elements[-7]
        d['s_kurtosis'] = elements[-3]
        d['s_omnibus_value'] = elements[-15]
        d['s_omnibus_prob'] = elements[-11]

        # Return
        return d

    def evaluate(self, alpha=0.05):
        """This method set all the variables into this class.

        Notes:
          - if instead of having the attribute series it is desired to set
            each element of the series as an attribute, just used the following
            statement: setattr(self, name, value).

          - Note the difference between the resid and wresid since they will
            also have different statistical properties. Furthermore, there is
            a vector with normalized residuals resid_pearson.

        @see: statsmodels.WLS
        @see: pyAMR.core.regression.RegressionResultsWrapper

        Parameters
        ----------
        alpha : the confidence interval

        Returns
        -------
        dictionary : map with all the parameters.
        """
        # Libraries.
        from statsmodels.iolib.summary import _getnames

        # Create series.
        d = {}

        # Add generic metrics.
        d['rsquared'] = self._raw.rsquared
        d['rsquared_adj'] = self._raw.rsquared_adj
        d['fvalue'] = self._raw.fvalue
        d['fprob'] = self._raw.f_pvalue
        d['aic'] = self._raw.aic
        d['bic'] = self._raw.bic
        d['llf'] = self._raw.llf
        d['mse_model'] = self._raw.mse_model
        d['mse_resid'] = self._raw.mse_resid
        d['mse_total'] = self._raw.mse_total

        # Create params information.
        params_data = zip(_getnames(self._raw)[1],
                          self._raw.params,
                          self._raw.bse,
                          self._raw.tvalues,
                          self._raw.pvalues,
                          self._raw.conf_int(alpha))

        # Add coefficients statistics.
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

        # Return
        return d

    # --------------------------------------------------------------------------
    #                           display methods
    # --------------------------------------------------------------------------
    def as_summary(self, **kwargs):
        """This method creates a summary string.
        """
        # Elements to split by.
        find = "=" * 78
        # Split and fill.
        smry = find.join(self._raw.summary(**kwargs).as_text().split(find)[:-1])
        # Add in new lines.
        smry += "Normal (N): %#25.3f   Prob(N): %#29.3f\n" % (self.m_nm_value,
                                                              self.m_nm_prob)
        smry += find
        # Return
        return smry

    # --------------------------------------------------------------------------
    #                          fit and predict methods
    # --------------------------------------------------------------------------
    def fit(self, endog, exog=None, trend='n',
            weights=None,
            W=None,
            **kwargs):
        """This method computes the WLS.

        @see statsmodels.regression.linear_model.WLS

        Parameters
        ----------
        endog : array-like
          The endogenous variable (aka. time series data)

        exog : array-like
          The exogenous variable (by default is the time t starting in 0)

        trend:  str-like, options = {c, n}
          Wether to add a constant or not.

        weights : array-like (optional)
          The weights for the weighted least square regression. If weights and
          W are both not note, the W instance will be used to transform the
          weights variables.

        W : object-like (optional)
          The instance to transform the weights. It must implement the
          function 'weights'.

        kwargs: dict-like
          The rest of the arguments to pass to the  __init__ and fit methods
          of the class statsmodels.WLS (see xxx)

        Returns
        -------
        object : OLSWrapper object.
        """
        # Create a time-series exogenous variable
        if exog is None:
            exog = np.arange(endog.size)

        # Format the exogenous variable to add constant.
        if trend == 'c':
            exog = sm.add_constant(copy.deepcopy(exog))

        # Compute weights from frequency
        if weights is not None and W is not None:
            weights = W.weights(weights)

        # Set uniform weights
        if weights is None:
            weights = np.ones(endog.size)

        # Save all newly created parameters
        kwargs['exog'] = exog
        kwargs['endog'] = endog
        kwargs['trend'] = trend
        kwargs['weights'] = weights
        kwargs['W'] = W

        # Call parents fit.
        super(WLSWrapper, self).fit(**kwargs)

        # Save results.
        return self

    def get_prediction(self, start=None, end=None, alpha=0.05, **kwargs):
        """This method predicts using the model.

        .. todo::

            Note that wls_predict_std has weights (those used in WLS) as
            an input parameter. However, these are not passed to the
            function. However, those weights are available for insample
            predictions but not for forecasting.

        Parameters
        ----------
        start : int (optional)
          The time t to start the prediction

        end : int (optional)
          The time t to end the prediction

        kwargs:
          The arguments to pass to the method get_prediction of the
          class statsmodels.WLS (see xxx)

        Returns
        -------
        time, prediction mean, prediction confidence interval
        """
        # Create exogenous variable.
        if start is not None or end is not None:
            kwargs['exog'] = self._exog(start, end)

        # Compute prediction.
        prediction = self._raw.get_prediction(**kwargs)

        # Add time.
        time = self._time(start=start, end=end)

        # Get plotting values
        mean = prediction.predicted_mean
        cito = prediction.conf_int()
        pito = self.pred_int(start=start, end=end, alpha=alpha)

        # Number of insample prediction
        ninsample = np.sum(time < self.endog.size)

        # Fill insamples
        pito[:ninsample, :] = cito[:ninsample, :]

        # Create result
        return np.column_stack((time, mean, pito)).T

    def line(self, x):
        """This method returns arrays to plot line and confidence intervals.
        """
        if 'const_coef' in self._result:
            return self.x1_coef * x + self.const_coef
        else:
            return self.x1_coef * x


if __name__ == '__main__':

    # Import
    import sys
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import statsmodels.robust.norms as norms

    # import weights.
    from pyamr.datasets.load import make_timeseries
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

    # Create method to compute weights from frequencies
    W = SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0)

    # ----------------------------
    # fit the model
    # ----------------------------
    # Note that the function fit will call M.weights(weights) inside and will
    # store the M converter in the instance. Therefore, the code execute is
    # equivalent to <weights=M.weights(f)> with the only difference being that
    # the weight converter is not saved.
    wls = WLSWrapper(estimator=sm.WLS).fit(exog=x[:80],
                                           endog=y[:80],
                                           trend='c',
                                           weights=f[:80],
                                           W=W,
                                           missing='raise')

    # Print series.
    print("\nSeries:")
    print(wls.as_series())

    # Print regression line.
    print("\nRegression line:")
    print(wls.line(np.arange(10)))

    # Print summary.
    print("\nSummary:")
    print(wls.as_summary())

    # -----------------
    # Save & Load
    # -----------------
    # File location
    # fname = '../../examples/saved/wls-sample.pickle'

    # Save
    # wls.save(fname=fname)

    # Load
    # wls = WLSWrapper().load(fname=fname)

    # -------------
    #  Example I
    # -------------
    # This example shows how to make predictions using the wrapper and how
    # to plot the resulting data. In addition, it compares the intervales
    # provided by get_prediction (confidence intervals) and the intervals
    # provided by wls_prediction_std (prediction intervals).
    #
    # To Do: Implement methods to compute CI and PI (see regression).

    # Variables.
    start, end = None, 180

    # Compute predictions (exogenous?).
    preds = wls.get_prediction(start=start, end=end)

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(11, 5))

    # Plotting confidence intervals
    # -----------------------------
    # Plot truth values.
    ax.plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
            markeredgecolor='k', markeredgewidth=0.5,
            markersize=5, linewidth=0.75, label='Observed')

    # Plot forecasted values.
    ax.plot(preds[0, :], preds[1, :], color='#FF0000', alpha=1.00,
            linewidth=2.0, label=wls._identifier(short=True))

    # Plot the confidence intervals.
    ax.fill_between(preds[0, :], preds[2, :],
                    preds[3, :],
                    color='r',
                    alpha=0.1)

    # Legend
    plt.legend()

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
    summary = WLSWrapper(estimator=sm.WLS).grid_search(grid_params=grid_params)

    # Show grid results
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
        axes[0].plot(preds[0, :], preds[1, :], linewidth=1.0,
                     label=model._identifier(short=True))

        # Plot the confidence intervals.
        axes[0].fill_between(preds[0, :], preds[2, :], preds[3, :], alpha=0.1)

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
