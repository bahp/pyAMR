###############################################################################
# Author: Bernard Hernandez
# Filename: 03-main-create-sari-idxs.py
# Description : This file contains differnent statistics used in time-series.
#               What it mainly does is to format the output of tests provided
#               by external libraries and return them in a dataframe.
#
# TODO: Move it to a module.
###############################################################################
# Libraries.
import math
import inspect
import warnings
import numpy as np
import pandas as pd

from scipy.stats import norm
from sklearn.model_selection import ParameterGrid


class BaseWrapper(object):
    # This is the name of the class.
    _name = 'BASE'

    # Main attributes of the class.
    _raw = None  # The raw object (statsmodels, scipy, ...)
    _result = {}  # Dictionary with metrics filled in self._init_result().
    _config = {}  # Dictioanry with configuration filled in
    _conkwargs = {}
    _fitkwargs = {}

    # ---------------------------------------------------------------------------
    #                               INIT METHOD
    # ---------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """Constructor empty defined just so grid_search works in main.

        Note: Emptying the configuration attribute is important because when
              calling grid_search, the self.__class__(args) calls the __init__
              method of the instance and updates the self._config dictionary.
              Since it has not been deepcopied, such modification will alter
              previous wrappers created during the grid search.
        """
        self._raw = None
        self._result = {}
        self._config = {}
        self._conkwargs = {}
        self._fitkwargs = {}

    def _identifier(self):
        """The name to identify this object."""
        return "%s" % self._name

    # ---------------------------------------------------------------------------
    #                        HELPER METHODS (PRIVATE)
    # ---------------------------------------------------------------------------
    def __getattr__(self, name):
        """This method allows to call series attributes from wrapper instance."""
        if name in self._result: return self._result[name]
        if name in self._config: return self._config[name]
        if name in self._conkwargs: return self._conkwargs[name]
        if name in self._fitkwargs: return self._fitkwargs[name]
        raise AttributeError

    def _cast_float(self, e):
        """This method casts an element to float when feasible.
        """
        try:
            return float(e)
        except:
            return e

    def _init_result(self):
        """This method fills self._results with the scores in self._raw.
        """
        pass

    def _init_config(self):
        """This method fills self._config with the configuration."""
        pass

    # ---------------------------------------------------------------------------
    #                              BASIC METHODS
    # ---------------------------------------------------------------------------
    def fargs(self, kwargs, function):
        """This method returns elements in kwargs which are function inputs."""
        # Get all parameters for the function.
        prms = inspect.getargspec(function)
        # Create dictionary and return
        return {k: kwargs[k] for k in prms.args if k in kwargs}

    def attrs(self):
        """This method returns all the defined attributes as tuples."""
        return inspect.getmembers(self, lambda a: not inspect.isroutine(a))

    def methods(self):
        """This method returns all the defined methods as tuples."""
        return inspect.getmembers(self, lambda a: inspect.isroutine(a))

    def save(self, fname):
        """This method saves the wrapper."""
        pickle.dump(self.__dict__, open(fname, "wb"))

    def load(self, fname):
        """This method loads the wrapper."""
        self.__dict__.clear()
        self.__dict__.update(pickle.load(open(fname, "rb")))
        return self

        # ---------------------------------------------------------------------------

    #                               GRID SEARCH
    # ---------------------------------------------------------------------------
    def grid_search(self, grid_params):
        """This method computes grid search.

        It creates all the possible combinations combining the arguments passed.
        Such arguments should be for the constructor and the fit methods. The
        results are stored in an array with the corresponding wrapper instances.

        Notes: The wrappers need to have the method fit implemented.

        Parameters
        ----------
        con_kwargs : arguments to be passed to the constructor method.
        fit_kwargs : arguments to be passed to the fit method.

        Returns
        -------
        summary : summary with all the elements.
        """
        # Create empty list.
        grid_results = []

        print("UEVAAA")

        # Loop for all possible combinations.
        for i, params in enumerate(ParameterGrid(grid_params)):
            try:
                # Create model and fit
                grid_results.append(self.__class__().fit(**params))
            except Exception as e:
                # Throw warning
                msg = "Iteration %s... failed: %s" % (i, e)
                warnings.warn(msg, RuntimeWarning)

        # Return summary.
        return grid_results

    # --------------------------------------------------------------------------
    #                       CREATES SUMMARY DATAFRAMES
    # --------------------------------------------------------------------------
    def from_list_dataframe(self, wrapper_list, **kwargs):
        """This methods creates a dataframe summary from a list.

        Parameters
        ----------
        wrapper_list : list with wrapper objects.
        flabel       : if include the class _name in the index.

        Returns
        -------
        summary : pandas dataframe.
        """
        # Create summary.
        summary = pd.DataFrame()

        # Loop filling the summary.
        for i, wrapper in enumerate(wrapper_list):
            results = wrapper.as_series(**kwargs).rename(i)
            summary = pd.concat([summary, results], axis=1, join='outer')

        # Return
        return summary.T

    def grid_search_dataframe(self, grid_params, **kwargs):
        """This method computes grid search and stores results in a dataframe.

        Parameters
        ----------
        con_kwargs : arguments to be passed to the constructor method.
        fit_kwargs : arguments to be passed to the fit method.

        Returns
        -------
        summary : summary with all the elements.
        """
        # Compute grid search.
        grid_results = self.grid_search(grid_params=grid_params)

        # Create empty dataframe.
        summary = pd.DataFrame()

        # Loop wrappers and fill it.
        for i, wrapper in enumerate(grid_results):
            results = wrapper.as_series(**kwargs).rename(i)
            summary = pd.concat([summary, results], axis=1, join='outer')

        # Return summary.
        return summary

    # ---------------------------------------------------------------------------
    #                                OVERRIDE
    # ---------------------------------------------------------------------------
    def as_series(self, flabel=True, label=None):
        """This method returns a series with all the information.

        Parameters
        ----------
        label : label to concatenate to index name (e.g. trend to label-trend).

        Returns
        -------
        series : pandas series with the results, configuration and model.
        """
        # Concatenate the configuration.
        s = {}
        s.update(self._result)
        s.update(self._config)
        s.update({'model': self._raw})
        s.update({'id': self._identifier()})
        # No label.
        if not flabel: return pd.Series(s)
        # Concat label at the begining of the index.
        label = self._name if label is None and hasattr(self, '_name') else label
        f = lambda x: "%s-%s" % (label.lower(), x)
        # Return
        return pd.Series(s).rename(index=f, copy=True)

    def as_summary(self):
        """This method displays the final summary."""
        # Call summary function from _raw (if exists).
        fsummary = getattr(self._raw, "summary", None)
        if callable(fsummary):
            return fsummary(self._raw)
        # Show the series information.
        return self.as_series().__repr__()

    def fit(self, **kwargs):
        """This method performs the fit."""
        # Empty results and update configuration.
        self._results = {}
        self._config.update(kwargs)
        return self


if __name__ == '__main__':
    # Set pandas configuration.
    pd.set_option('display.max_colwidth', 14)
    pd.set_option('display.width', 80)
    pd.set_option('display.precision', 4)

    # Create and fill a base statistic wrapper.
    w = BaseWrapper()
    w._raw = object()
    w._config = {'p': 2, 'c': 4}
    w._result = {'score': 25}

    # Get attributes tuple list.
    print(w.attrs())

    # Get methods tuple list.
    print(w.methods())

    # Get series with parameters.
    print(w.as_series())

    # Print summary.
    print(w.as_summary())

    # Quick access to an attribute.
    print(w.score)

    # -----------
    # Grid search
    # -----------
    # Parameters
    con_params = {
        'con_1': [True],
        'con_2': ['1', '2'],
    }
    fit_params = {
        'fit_1': [5]
    }

    # Grid search method
    summary = w.grid_search_dataframe(con_kwargs=con_params,
                                      fit_kwargs=fit_params)

    # Show
    print(summary)
