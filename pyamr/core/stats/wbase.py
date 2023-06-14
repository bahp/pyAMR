###############################################################################
# Author: Bernard Hernandez
# Filename: 03-main-create-sari-idxs.py
# Description : This file contains differnent statistics used in time-series.
#               What it mainly does is to format the output of tests provided
#               by external libraries and return them in a dataframe.
#
# TODO: Move it to a module.
###############################################################################
# Libraries
import math
import pickle
import inspect
import warnings
import numpy as np
import pandas as pd
# import cPickle as pickle # not needed in python 3.x

# Specific
from copy import deepcopy
from sklearn.model_selection import ParameterGrid


# -----------------------------------------------------------------------------
#                              helper methods
# -----------------------------------------------------------------------------
def fargs(function, kwargs):
    """Finds parameters in kwargs tho use in function.

    Parameters
    ----------
    function : callable
      The function

    kwargs : dict-like
      The parameters and corresponding values.

    Returns
    -------
    """
    # Get all parameters for the function.
    prms = inspect.getfullargspec(function)
    # Create dictionary and return
    return {k: kwargs[k] for k in prms.args if k in kwargs}


def getargspecdict(instance, funcname):
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
        prms = inspect.getfullargspec(func)
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


# def attrs(self):
#  """This method returns all the defined attributes as tuples."""
#  return inspect.getmembers(self, lambda a: not inspect.isroutine(a))

# def methods(self):
#  """This method returns all the defined methods as tuples."""
#  return inspect.getmembers(self, lambda a: inspect.isroutine(a))


class BaseWrapper(object):
    """Base Wrapper
    """

    # Main attributes of the class.
    _raw = None  # The raw object (statsmodels, scipy, ...)
    _result = {}  # Dictionary with metrics filled in self._init_result().
    _config = {}  # Dictioanry with configuration filled in
    _conkwargs = {}
    _fitkwargs = {}

    def __init__(self, estimator=None, evaluate=True):
        """Constructor empty defined just so grid_search works in main.

        Note: Emptying the configuration attribute is important because when
              calling grid_search, the self.__class__(args) calls the __init__
              method of the instance and updates the self._config dictionary.
              Since it might not have been deepcopied, such modification will
              alter previous wrappers created during the grid search.
        """
        # Store the estimator
        self.estimator = estimator

        # Set the name
        self._name = self.__class__.__name__.replace('Wrapper', '')

        # Initialize the containers
        self._raw = None
        self._result = {}
        self._config = {}

    # ---------------------------------------------------------------------------
    #                            helper methods
    # ---------------------------------------------------------------------------
    def _empty(self):
        """This method empties the class."""
        self._raw = None
        self._result = {}
        self._config = {}

    def _identifier(self):
        """The name to identify this object."""
        return "%s" % self._name

    def __getattr__(self, name):
        """This method allows to retrieve series attributes with dot notation.

        .. note::

          The __getattr__ method is called only when __getattribute__ method was
          unsuccessful. As such, attributes such as .__class__ can still be
          called even though this method is overriden.

        Parameters
        ----------
        name : string
          The name of the attribute to retrieve.

        """
        # Retrieve the attribute
        if name in self._result: return self._result[name]
        if name in self._config: return self._config[name]
        # Raise error
        raise AttributeError("'%s' object has no attribute '%s'" % \
                             (self.__class__.__name__, name))

    # ---------------------------------------------------------------------------
    #                               save and load
    # ---------------------------------------------------------------------------
    def save(self, fname):
        """This method saves the wrapper."""
        pickle.dump(self.__dict__, open(fname, "wb"))

    def load(self, fname):
        """This method loads the wrapper."""
        self.__dict__.clear()
        self.__dict__.update(pickle.load(open(fname, "rb")))
        return self

    # ---------------------------------------------------------------------------
    #                               grid search
    # ---------------------------------------------------------------------------
    def grid_search(self, grid_params, verbose=0):
        """This method computes grid search.

        .. note: The wrapper needs to have the method ``fit`` implemented.

        Parameters
        ----------
        grid_params : array-like
          The grid of parameters to search.

        verbose : int
          Wether to show the progress of the search.

        Returns
        -------
        summary : summary with all the elements.
        """

        # Create empty list.
        wrappers = []

        # Create all possible combinations
        parameters = ParameterGrid(grid_params)

        # Number of combinations
        n = len(parameters)

        # Loop for all possible combinations.
        for i, params in enumerate(parameters):
            try:
                # Deep copy the object.
                copied = deepcopy(self)
                # Create model and fit
                wrappers.append(copied.fit(**params))
                # Show information
                if (verbose > 0):
                    print("%d/%d. %s" % (i + 1, n, copied._identifier()))

            except Exception as e:
                # Create message and raise warning
                msg = "%d/%d. %s ... failed: %s" % (i + 1, n, copied._identifier(), e)
                print(msg)

        # Return summary.
        return wrappers

    def from_list_dataframe(self, wrapper_list, **kwargs):
        """This methods creates a dataframe summary from a list.

        Parameters
        ----------
        wrapper_list : array-like
          The list with wrapper objects.

        flabel : boolean
          Wether to include a label before the attributes.

        label : string
          The label to include before the attributes. By default it includes
          the value of the attribute `self._name` in lowercase.

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

    # ---------------------------------------------------------------------------
    #                                OVERRIDE
    # ---------------------------------------------------------------------------
    def as_series(self, flabel=True, label=None):
        """This method returns a series with all the information.

        Parameters
        ----------
        flabel : boolean
          Wether to include a label before the attributes.

        label : string
          The label to include before the attributes. By default it includes
          the value of the attribute `self._name` in lowercase.

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

        # Create the label to include
        if label is None and hasattr(self, '_name'):
            label = self._name.lower()
        else:
            label = str(label)

        # format label
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

    # ---------------------------------------------------------------------------
    #                           method to override
    # ---------------------------------------------------------------------------
    def evaluate(self, **kwargs):
        """
        """
        # Return empty.
        return {}

    # ---------------------------------------------------------------------------
    #                                fit methods
    # ---------------------------------------------------------------------------
    def _fit_funct(self, **kwargs):
        """
        """
        # Get arguments
        arguments = fargs(self.estimator, kwargs)
        # Call function
        self._raw = self.estimator(**arguments)

    def _fit_class(self, **kwargs):
        """
        """
        # Get arguments
        conkwargs = fargs(self.estimator.__init__, kwargs)
        fitkwargs = fargs(self.estimator.fit, kwargs)
        # Call function
        self._raw = self.estimator(**conkwargs).fit(**fitkwargs)

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

        # Evaluate the model
        if self.evaluate:
            self._result = self.evaluate()

        # Return
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
    #print(w.attrs())

    # Get methods tuple list.
    #print(w.methods())

    # Get series with parameters.
    #print(w.as_series())

    # Print summary.
    #print(w.as_summary())

    # Quick access to an attribute.
    #print(w.score)

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
    #summary = w.grid_search_dataframe(con_kwargs=con_params,
    #                                  fit_kwargs=fit_params)

    # Show
    #print(summary)
