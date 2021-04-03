################################################################################
# Author:
# Date:
# Description:
#
#
#
# Copyright:
#
# 
################################################################################
# Import libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own
from pyamr.core.freq import Frequency

# -------------------------------------------------------------------------
#                            helper methods
# -------------------------------------------------------------------------
def _check_dataframe(dataframe):
  """Ensure the three columns are available.
  """
  # Copy
  aux = dataframe.copy(deep=True)

  # Add missing columns
  if not 'resistant' in dataframe:
    aux['resistant'] = 0
  if not 'intermediate' in  dataframe:
    aux['intermediate'] = 0
  if not 'sensitive' in dataframe:
    aux['sensitivity'] = 0

  # return
  return aux

def sari_soft(dataframe):
  """
  """
  # Check
  dataframe = _check_dataframe(dataframe)
  # Get values
  r = dataframe['resistant']
  i = dataframe['intermediate']
  s = dataframe['sensitive']
  # Compute
  return r / (r+i+s)

def sari_medium(dataframe):
  """
  """
  # Check
  dataframe = _check_dataframe(dataframe)
  # Get values
  r = dataframe['resistant']
  s = dataframe['sensitive']
  # Compute
  return r / (r+s)

def sari_hard(dataframe):
  """
  """
  # Check
  dataframe = _check_dataframe(dataframe)
  # Get values
  r = dataframe['resistant']
  i = dataframe['intermediate']
  s = dataframe['sensitive']
  # Compute
  return (r+i) / (r+i+s)

def sari_whard(dataframe, w=0.5):
  """
  """
  # Check
  dataframe = _check_dataframe(dataframe)
  # Get values
  r = dataframe['resistant']
  i = dataframe['intermediate']
  s = dataframe['sensitive']
  # Compute
  return (r+w*i) / (r+w*i+s)  



def sari(dataframe, strategy='hard', **kwargs):
    """Computes the sari index.

    Parameters
    ----------
    dataframe: pd.DataFrame
        A dataframe with the susceptibility test interpretations
        as columns. The default strategies expect the following
        columns: 'sensitive', 'intermediate', 'resistant'.

    strategy: string or func (default hard)
        The method used to compute sari. The possible options
        are 'soft', 'medium' and 'hard'. In addition, a function
        with the following signature can be passed:
           dataframe
           arguments

    **kwargs: arguments to pass the strategy function.

    Returns
    --------
    """
    # Ensure that exists
    aux = _check_dataframe(dataframe)

    # Extract vectors
    r = aux['resistant']
    i = aux['intermediate']
    s = aux['sensitive']

    # Call the function
    if callable(strategy):
        return strategy(aux, **kwargs)

    # Check strategy.
    if strategy not in ['soft', 'medium', 'hard']:
        raise ValueError("""
              The strategy '{0}' is not supported and
              therefore the strategy 'hard' will be used.""" \
              .format(strategy))

    # Compute
    if strategy == 'hard':
        return (r + i) / (r + i + s)
    elif strategy == 'medium':
        return r / (r + s)
    elif strategy == 'soft':
        return r / (r + i + s)




class SARI:

    # Attributes
    c_spe = 'SPECIMEN'
    c_org = 'SPECIE'
    c_abx = 'ANTIBIOTIC'
    c_dat = 'DATE'
    c_out = 'SENSITIVITY'



    def __init__(self, groupby=[c_spe,
                                c_org,
                                c_abx,
                                c_out]):
        """Constructor

        Parameters
        ----------

        Returns
        --------
        """
        self.groupby = groupby

    def compute(self, dataframe, shift=None, period=None, cdate=None,
                return_frequencies=True, **kwargs):
        """Computes single antibiotic resistance index.

        .. todo: Add parameters to rolling!
        .. todo: Place value at the left, center, right of window?
        .. todo: Ensure that works when time gaps present!
        .. todo: Carefull with various indexes!

        Parameters
        ----------

        Returns
        -------

        """

        # Copy DataFrame
        aux = dataframe.copy(deep=True)

        # If dates.... warning if na
        # Warning nan for elements in groupby!

        # Create grouper
        grouper = []
        if shift is not None:
            grouper = [pd.Grouper(freq=shift, key=cdate)]
        grouper = grouper + self.groupby

        # ------------------------------------------
        # Frequencies
        # ------------------------------------------
        # Compute frequencies
        if shift is None:
            freqs = aux.groupby(grouper) \
                .size().unstack().fillna(0)

        else:
            # Format as datetime
            aux[cdate] = pd.to_datetime(aux[cdate])

            # Compute frequencies
            freqs = aux.groupby(grouper) \
                .size().unstack().reset_index() \
                .set_index(cdate).groupby(grouper[1:-1]) \
                .rolling(window=period, min_periods=1) \
                .sum().fillna(0)

        # -------------------
        # Sari
        # -------------------
        # Compute sari
        s = sari(freqs, **kwargs)

        # Return
        if return_frequencies:
            freqs['freq'] = freqs.sum(axis=1)
            freqs['sari'] = sari(freqs, **kwargs)
            return freqs
        return s.rename('sari')




# Default methods
_DEFAULT_STRATEGIES = {
  'soft': sari_soft,
  'medium': sari_medium,
  'hard': sari_hard
}



class SARI_old():

  # Attributes
  c_abx = 'ANTIBIOTIC'
  c_org = 'SPECIE'
  c_dat = 'DATE' 
  c_out = 'SENSITIVITY'


  # -------------------------------------------------------------------------
  #
  # -------------------------------------------------------------------------
  def __init__(self, strategy='hard'):
    """The constructor.

    Parameters
    ----------
    strategy : string or function
      The mode to compute the single antibiotic resistance index. 
      There are three predefined strategies: 
        (i) soft as    R / R+I+S 
        (ii) medium as R / R+S 
        (iii) hard as  R+I / R+I+S
        (iv) other     R+0.5I / R+0.5I+S

    Returns
    -------
    """
    if isinstance(strategy, str):

      # Check that the strategy exists
      if not strategy in _DEFAULT_STRATEGIES.keys():
        raise ValueError("The strategy selected (%s) is not supported. "
                         "Please use one of the following [%s] "
                         % _DEFAULT_STRATEGIES.keys())

      # Set strategy
      self.func = _DEFAULT_STRATEGIES[strategy]


    #if callable(strategy):
    #  self.func = strategy


  # -------------------------------------------------------------------------
  #
  # -------------------------------------------------------------------------
  def compute(self, dataframe):
    """This method computes the single antibitic resistance index
    """
    # Copy dataframe
    dataframe = dataframe.copy(deep=True)

    # Add column with sari
    dataframe['sari'] = self.func(dataframe)

    # Return
    return dataframe
    








if __name__ == '__main__':

  # Import libraries
  import sys
  import matplotlib as mpl
  import matplotlib.pyplot as plt

  # Import specific libraries
  from pyamr.datasets import load

  # Set matplotlib
  mpl.rcParams['xtick.labelsize'] = 9
  mpl.rcParams['ytick.labelsize'] = 9
  mpl.rcParams['axes.titlesize'] = 11
  mpl.rcParams['legend.fontsize'] = 9

  # -----------------------
  # Load data
  # ----------------------- 
  # Load sample data
  data = load.dataset_epicimpoc_susceptibility_year(nrows=1000000)

  # Keep only relevant columns
  data = data[['antibioticCode',
               'organismCode',
               'dateReceived',
               'sensitivity']]


  # Filter for two examples
  is_org = data['organismCode']=='ECOL'
  is_abx = data['antibioticCode'].isin(['AAUG'])
  data = data[is_abx & is_org]

  # -------------------------
  # Create frequency instance
  # -------------------------
  # Create instance
  freq = Frequency(column_antibiotic='antibioticCode',
                   column_organism='organismCode',
                   column_date='dateReceived',
                   column_outcome='sensitivity')

  
  # Compute frequencies daily
  daily = freq.compute(data, strategy='ITI', 
                               by_category='pairs', 
                               fs='1D')

  # Compute frequencies monthly
  monthly = freq.compute(data, strategy='ITI', 
                               by_category='pairs', 
                               fs='1M')

  # Compute frequencies overlapping
  oti_1 = freq.compute(data, strategy='OTI', 
                             by_category='pairs', 
                             wshift='1D',
                             wsize=90)

  # -------------------------
  # Create sari instance
  # -------------------------
  # Create instance
  sari_daily = SARI(strategy='hard').compute(daily)
  sari_monthly = SARI(strategy='hard').compute(monthly)
  sari_oti_1 = SARI(strategy='hard').compute(oti_1)

  # -------
  # Plot
  # -------
  # Show comparison for each pair
  f, axes = plt.subplots(4, 1, figsize=(15,8))

  # Flatten axes
  axes = axes.flatten()

  # Plot ITI (monthly)
  for i,(pair, group) in enumerate(sari_daily.groupby(level=[0,1])):
    group.index = group.index.droplevel([0,1])
    group['sari'].plot(marker='o', ms=3, label=pair, 
      linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3, 
      ax=axes[0])

  # Plot ITI (monthly)
  for i,(pair, group) in enumerate(sari_monthly.groupby(level=[0,1])):
    group.index = group.index.droplevel([0,1])
    group['sari'].plot(marker='o', ms=3, label=pair, 
      linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3, 
      ax=axes[1])

  # Plot OTI (daily with size 30)
  for i,(pair, group) in enumerate(sari_oti_1.groupby(level=[0,1])):
    group.index = group.index.droplevel([0,1])
    group['sari'].plot(marker='o', ms=3, label=pair, 
      linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3, 
      ax=axes[2])

  # Set legend
  for ax in axes:
    ax.legend()
    ax.set_xlabel('')
    ax.grid(True)

  # Set titles
  axes[0].set_ylabel('Daily')
  axes[1].set_ylabel('Monthly')
  axes[2].set_ylabel('OTI(1D,90)')

  # Show
  plt.show()