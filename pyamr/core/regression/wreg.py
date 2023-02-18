###############################################################################
# Author: Bernard Hernandez
# Filename: 03-main-create-sari-idxs.py
# Description : This file contains differnent statistics used in time-series.
#               What it mainly does is to format the output of tests provided
#               by external libraries and return them in a dataframe.
#
# TODO: Move it to a module.
###############################################################################
# Forces decimals on divisions.
from __future__ import division

# Libraries
import sys
import math
import inspect
import numpy as np
import pandas as pd
import statsmodels.api as sm

# External libraries
from scipy.stats import norm
from sklearn.model_selection import ParameterGrid

# Import base wrapper
from pyamr.core.stats.wbase import fargs
from pyamr.core.stats.wbase import BaseWrapper


# ---------------------------------------------------------------------------
#                             helper methods
# ---------------------------------------------------------------------------
def _forecast_error(sigma2, arparams, maparams, steps):
    """This method forecasts the error.

    Used in ARIMAWrapper.

    .. note::

        These functions have been extracted from the ``_forecast_conf_int()``
        and ``_forecast_error()`` implemented in the the class ARIMAResults
        within statsmodels.ts.arima_model. As such, it produces the
        same confidence intervals as those printed using the method
        ``plot_predict()``.

    Parameters
    ----------

    Returns
    -------
    """
    # Libraries.
    from statsmodels.tsa.arima_process import arma2ma
    # Compute error.
    ma_rep = arma2ma(np.r_[1, -arparams],
                     np.r_[1, maparams], lags=steps)  # nobs removed!
    fcasterr = np.sqrt(sigma2 * np.cumsum(ma_rep ** 2))
    # Return
    return fcasterr


def _forecast_conf_int(forecast, fcasterr, alpha=0.05):
    """This method forecasts the confidence interval.

    Parameters
    ----------

    Returns
    -------
    """
    # Libraries.
    from scipy.stats import t, norm
    # Compute confidence intervals
    const = norm.ppf(1 - alpha / 2.)
    conf_int = np.c_[forecast - const * fcasterr,
                     forecast + const * fcasterr]
    # Return
    return conf_int


def _insample_conf_int(forecast, resid, alpha=0.05):
    """This function computes a basic confidence interval.

    Note: It might not be the adecuate way of computing it.

    Parameters
    ----------
    forecast : the forecasted values.
    alpha    : the alpha value selected.

    Returns
    -------
    cilo :
    ciup :
    """
    # Compute variables.
    const = norm.ppf(1.0 - alpha / 2.0)
    mu = np.mean(resid)
    std = np.std(resid)
    c = const * (std / math.sqrt(resid.shape[0]))
    # Compute confidence interval.
    conf_int = np.c_[forecast - c, forecast + c]
    # Return
    return conf_int


class RegressionWrapper(BaseWrapper):
    """Description...


    """
    # Attribute
    _resid = None

    # ---------------------------------------------------------------------------
    #                             HELPER METHODS
    # ---------------------------------------------------------------------------
    def _init_config(self):
        """This method fills self._config with the configuration."""
        # Create dir.
        d = {}
        # Find attributes values for interesting methods.
        d.update(self._getargspecdict(self._raw.model, '__init__'))
        d.update(self._getargspecdict(self._raw.model, 'fit'))
        # Return
        return d

    def _getargspecdict(self, instance, funcname):
        """This method creates a dictionary with pairs name and value.

        Parameters
        ----------
        instance : object with values
        funcname : function which parameters name will be looked for.

        Returns
        -------
        tpls : dictionary with argument name and value.
        """
        try:
            # Get argument parameters.
            func = getattr(instance, funcname, None)
            prms = inspect.getargspec(func)
            tpls = {}
            # Create and fill dictionary
            for name in prms.args:
                if name == 'self': continue
                tpls[name] = getattr(instance, name, None)
            # Return
            return tpls
        except Exception as e:
            # Print
            print("[Exception at _getargspecdict : %s" % e)
            # Return
            return {}

    def conf_int_insample(self, predictions, alpha=0.05):
        """Computes the in-sample confidence interval.

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
        return _insample_conf_int(forecast=predictions,
                                  resid=self._resid,
                                  alpha=alpha)

    # ---------------------------------------------------------------------------
    #              STATISTIC METHODS FOR REGRESSION ANALYSIS
    # ---------------------------------------------------------------------------
    def _resid_stats(self, resid=None, alpha=0.05):
        """This method computes basic stats on the residuals

        Parameters
        ----------
        resid : array-like
          The residuals to perform the stats on.

        alpha : int-like
          The alpha selected.

        Returns
        -------
        dictionary with the stats for the residuals
        """
        # Check if resid is passed.
        if resid is None:
            resid = self._resid

        # No resid to work with.
        if resid is None:
            return {}

        # Create series.
        d = {}

        # Compute autoc-orrelation (durbin-watson)
        from statsmodels.stats.stattools import durbin_watson
        d['m_dw'] = durbin_watson(resid)

        # Compute normalility (jarque bera).
        from statsmodels.stats.stattools import jarque_bera
        jb_value, jb_prob, skew, kurtosis = jarque_bera(resid)
        d['m_jb_value'] = jb_value
        d['m_jb_prob'] = jb_prob
        d['m_skew'] = skew
        d['m_kurtosis'] = kurtosis

        try:
            # Compute normal test (normal test)
            from scipy.stats import normaltest
            nm_value, nm_prob = normaltest(resid)
            d['m_nm_value'] = nm_value
            d['m_nm_prob'] = nm_prob
        except ValueError as e:
            print(e)
            d['m_nm_value'] = np.inf
            d['m_nm_prob'] = np.inf


        # Compute the kolmogorov-smirnov test.
        from scipy.stats import kstest
        ks_value, ks_prob = kstest(resid, 'norm')
        d['m_ks_value'] = ks_value
        d['m_ks_prob'] = ks_prob

        try:
            # Compute the shapiro-wilkinson test.
            from scipy.stats import shapiro
            sh_value, sh_prob = shapiro(resid)
            d['m_shp_value'] = sh_value
            d['m_shp_prob'] = sh_prob
        except ValueError as e:
            print(e)
            d['m_shp_value'] = np.inf
            d['m_shp_prob'] = np.inf

        # Compute anderson-darling.
        # The null hypothesis (sample data is drawn from a population that
        # follows a particular distribution; in this case normal) can be rejected
        # if the statistic es larger than the critical values for an specified
        # significance level.
        from scipy.stats import anderson
        ad_value, ad_cv, ad_sl = anderson(resid)
        d['m_ad_value'] = ad_value
        d['m_ad_nnorm'] = ad_value < ad_cv[2]

        # Return
        return d

    def _exog(self, start=None, end=None):
        """This method generates the exogenous variable time.

        Note: it is only used for those regression methods that do not support
        the parameters start and end in the prediction (wls, ols, rlm, ...).
        On the other side, this method is not necessary for ARIMA since they
        already support this notation.

        .. note:: end is included (see _time()).

        Parameters
        ----------
        start : int (optional)
          The time t to start the prediction

        end : int (optional)
          The time t to end the prediction

        Returns
        -------
        the exogenous variable
        """
        # Default start and end.
        exog = self._time(start=start, end=end)
        # Add constant if required.
        trend = getattr(self, 'trend', None)
        # Return exog without constant
        if trend is None or trend == 'ct':
            return exog
        # Add constant.
        exog = sm.add_constant(exog)
        # Return
        return exog

    def _time(self, start=None, end=None):
        """This method generates the time variable.

        .. note::

          The value indicated by 'end' is included. This is that way
          to match with the implementation of ARIMA from statsmodels.

        Parameters
        ----------
        start : int (optional)
          The time t to start the prediction

        end : int (optional)
          The time t to finish the prediction.

        Returns
        -------
        """
        start = 0 if start is None else start
        end = len(self.endog) if end is None else end + 1
        # Generate time variable.
        return np.arange(start, end, 1)

    def resid(self):
        """Get the residual"""
        if hasattr(self._raw, 'resid'):
            return self._raw.resid

    def fit(self, **kwargs):
        """This method performs the fit.

        Parameters
        ----------
        kwargs : dict-like
          The arguments that will be passed to the method.

        Returns
        -------

        """
        # Empty the class
        self._empty()
        # Update the configuration
        self._config.update(kwargs)

        # Fit the model
        if inspect.isfunction(self.estimator):
            self._fit_funct(**kwargs)
        elif inspect.isclass(self.estimator):
            self._fit_class(**kwargs)

        # Set the residual
        self._resid = self.resid()

        # Evaluate the model
        if self.evaluate:
            self._result = self.evaluate()

        # Return
        return self


if __name__ == '__main__':
    # Constants
    length = 100
    offset = 100
    slope = 10

    # Create time-series.
    x = np.arange(length)
    n = np.random.randn(length) * 10
    y_orig = slope * x + offset + n
    y_pred = slope * x + offset

    # Create and fill a base statistic wrapper.
    w = RegressionWrapper()
    w._resid = y_orig - y_pred

    # Print resid stats
    print(pd.Series(w._resid_stats()))

    # Print resid confidence intervals
    print(w.conf_int_insample(forecast=y_pred))
