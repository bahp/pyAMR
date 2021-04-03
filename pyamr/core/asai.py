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
from __future__ import division 

# Libraries
import sys
import warnings
import numpy as np 
import pandas as pd 

# ------------------------------------------------------------------------------
#                                 methods
# ------------------------------------------------------------------------------
def _check_asai_weights_genus(dataframe):
  """Checks that the weights for each genus add up to one.

  Parameters
  ----------
  dataframe : dtaframe-like
    The dataframe whose columns must be checked

  Returns
  -------
  raise error  
  """
  # Compute weights per genus
  weights = dataframe.groupby(by='GENUS')['W_SPECIE'].sum()
  weights = np.round(weights, decimals=10)

  # Check that all add up to one
  if not (weights==1).all():
    raise TypeError("The weights (W_SPECIE) for each genus should add up to "
                    "one. Please review these weights since they are not "
                    "valid. \n%s" % weights)


def _check_asai_weights_specie(dataframe):
  """Check that the weights for all the species add up to one.

  Parameters
  ----------
  dataframe : dtaframe-like
    The dataframe whose columns must be checked

  Returns
  -------
  raise error
  """
  # Compute weights per species
  unique = dataframe.groupby(by='GENUS')['W_GENUS'].nunique()
  weights = dataframe.groupby(by='GENUS')['W_GENUS'].mean()
  merged = pd.concat([unique, weights], axis=1)
  merged.columns = ['UNIQUE', 'W_GENUS']

  # Check only one weight is given for each genus
  if not (unique==1).all():
    raise TypeError("The weights (W_GENUS) should be equal for all the rows "
                    "with a same genus value. Please ensure that the number "
                    "of unique elements is always 1. \n%s" % merged)

  # Check that weights add up to one
  if not (np.round(np.sum(weights), decimals=10)==1):
    return TypeError("The weights (W_GENUS) should add up to one. Please "
                     "review these weights since they are not valid. "
                     "\n%s" % weights)


def _check_asai_dataframe_columns(dataframe, required_columns):
  """This method checks that the dataframe has all attributes.

  Parameters
  -----------
  dataframe : pandas DataFrame
    The dataframe containing the information.

  attributes :
    The required columns

  Returns
  -------
  exit the program
  """
  # Find missing columns
  missing = list(set(required_columns) - set(dataframe.columns))
  # There are missing columns
  if not missing: return
  # Raise an error
  raise TypeError("The dataframe passed as argument is missing the "
                  "following columns: %s. Please correct this issue." 
                  % missing)


def _asai(dataframe, threshold=None, weights='uniform'):
  """Computes the antimicrobial spectrum of activity.

  .. todo: There is an error when W_GENUS = 1 / GENUS.nunique()

  Parameters
  ----------
  dataframe : dataframe-like
    The dataframe containing the information to compute the asai index. The 
    following columns are required [SPECIE, GENUS, RESISTANCE]. In addition,
    the effective threshold, genus weight and specie weight can be specied
    using the following columns [THRESHOLD, W_GENUS, W_SPECIE]. Note that
    the weights must add up to one.

  threshold : number
    The number to set a common threshold.

  weights : string
    Method used to compute the weights. The possible values are uniform and
    proportional. In order to use proportional a column with the frequency
    for each specie must be included in the dataframe.


  Returns
  -------
  dataframe
  """
  # Check that the input is a dataframe
  if not isinstance(dataframe, pd.DataFrame):
    raise TypeError("The instance passed as argument needs to be a pandas "
                    "DataFrame. Instead, a <%s> was found. Please convert "
                    "the input accordingly." % type(dataframe))

  # Add fixed threshold
  if threshold is not None:
    dataframe['THRESHOLD'] = threshold

  # Add weights
  if weights == 'uniform':
    # Set uniform weights
    dataframe = dataframe.set_index(keys=['GENUS'], drop=False)
    dataframe['W_GENUS'] = 1. / dataframe.GENUS.nunique()
    dataframe['W_SPECIE'] = 1. / dataframe.SPECIE.groupby(level=0).count()
    dataframe = dataframe.reset_index(drop=True)

  # Required columns
  required = ['RESISTANCE', 'THRESHOLD', 'W_GENUS', 'W_SPECIE']

  # Check that the weights add up to one.
  _check_asai_dataframe_columns(dataframe, required_columns=required)
  _check_asai_weights_genus(dataframe)
  _check_asai_weights_specie(dataframe)

  # Select data
  resistance = dataframe.RESISTANCE
  threshold = dataframe.THRESHOLD
  weights_genus = dataframe.W_GENUS
  weights_specie = dataframe.W_SPECIE


  # Create results
  d = {'N_GENUS': dataframe.GENUS.nunique(),
       'N_SPECIE': dataframe.SPECIE.nunique(),
       'ASAI_SCORE': _asai_score(weights_genus,
                                 weights_specie,
                                 resistance, 
                                 threshold)}

  # Compute ASAI.
  return pd.Series(d)


def _asai_score(weights_genus, weights_specie, resistance, threshold):
  """Computes the asai score.

  Parameters
  ----------
  weights_genus : array-like
    The weight associated to each of the genus

  weights_specie : array-like
    The weight associated to each of the species

  resistance : array-like

    The resistances
  threshold : array-like
    The thresholds

  Returns
  -------
  asai score
  """
  return np.sum(weights_genus*weights_specie*(resistance<=threshold))


def asai(dataframe, weights=None, threshold=None, tol=1e-6, verbose=0):
    """Computes the ASAI.

    .. warning:: Should the duplicated check only for the columns
                 GENUS and SPECIE? What if we do not group by
                 antibiotic? It has to be unique for the antibiotic
                 also. It is up to the user to make the right use
                 of this?

    Parameters
    ----------
    dataframe: pd.DataFrame
        The pandas dataframe with the information. The following columns
        are always required [RESISTANCE, GENUS and SPECIE]. In addition,
        [W_GENUS and W_SPECIE] are required if weights is None.

    weights: string (default None)
        The method to automatically compute the weights. The methods
        supported are 'uniform' in which all genus have the same
        weights and all species within a genus have the same weight.
        In order to use the specified weights [W_GENUS, W_SPECIE]
        keep weights as None. Please remember that the following
        rules must be fulfilled by the weights:
           - consistent weight for a given genus
           - all genus weights must add up to one.
           - all specie weights within a genus must add up to one.

    threshold: float (default None)
        The threshold value to consider the microorganism as
        resistant to the antimicrobial. Thus, for a threshold of 0.5,
        if a pair <o,a> has a resistance value of 0.4, the microorganism
        will be considered sensitive to the antimicrobial and will
        count towards the ASAI computation. In order to use specific
        thresholds [THRESHOLD] keep threshold as None.

    tol: float (default 1e-6)
        The tolerance in order to check that all conditions (uniqueness
        and sums) are satisfied. Note that that float precision varies
        and therefore not always adds up to exactly one.

    verbose: int (default 0)
        The level of verbosity.

    Returns
    -------
    """
    # Required columns
    required = ['RESISTANCE', 'GENUS', 'SPECIE']

    # Add weight columns
    if weights is None:
        required += ['W_GENUS', 'W_SPECIE']

    # Bad input type
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The instance passed as argument needs to be a pandas "
                        "DataFrame. Instead, a <%s> was found. Please convert "
                        "the input accordingly." % type(dataframe))

    # Check columns
    if set(required).difference(dataframe.columns):
        raise ValueError("The following columns are missing: {0} " \
                .format(set(required).difference(dataframe.columns)))

    # Check duplicates
    if dataframe.duplicated().any():
        raise ValueError("There are duplicate rows in the dataframe.")

    # Copy dataframe
    aux = dataframe.copy(deep=True)

    # Check threshold
    if 'THRESHOLD' in aux.columns:
        if threshold is not None:
            warnings.warn("""\n
                  The threshold has been defined both as an 
                  input parameter (threshold={0}) and a dataframe 
                  column 'THRESHOLD'. The latter will be used."""
                  .format(threshold))
    else:
        if threshold is None:
            warnings.warn("""\n
                  The threshold has not been defined using either 
                  an input parameter (threshold={0}) or a column in the 
                  dataframe 'THRESHOLD'. Thus a default threshold value 
                  of '0.5' will be used.""".format(threshold))
            threshold = 0.5
        aux['THRESHOLD'] = threshold

    # Set uniform weights
    if weights == 'uniform':
        # Set uniform weights
        aux['W_GENUS'] = 1. / aux.GENUS.nunique()
        aux['W_SPECIE'] = 1. / aux.GENUS.map(
            aux.groupby(['GENUS']).SPECIE.count())

    # Set frequency weights
    if weights == 'frequency':
        # Set frequency weights
        fgn = aux.groupby(['GENUS']).FREQUENCY.sum()
        aux['S_GENUS'] = aux.GENUS.map(fgn)
        aux['W_GENUS'] = aux.GENUS.map(fgn / fgn.sum())
        aux['W_SPECIE'] = aux.FREQUENCY / aux.S_GENUS

    # Check sums
    report = pd.DataFrame()
    report['W_GENUS_UNIQUE_OK'] = aux.groupby('GENUS').W_GENUS.nunique()
    report['W_GENUS_SUM_OK'] = aux.groupby('GENUS').head(1).W_GENUS.sum()
    report['W_SPECIE_SUM_OK'] = aux.groupby(['GENUS']).W_SPECIE.sum()

    # Condition
    condition = (1 - report).abs() < tol

    # Report
    if not condition.all().all():
        raise ValueError("""
            The weights imputed do not fulfill all the requirements. Please
            check the report below and correct the weights accordingly. Note
            a given genus must have a consistent weight and the sum of weights
            must add up to 1.\n\n\t\t{0}""" \
            .format(condition.to_string().replace("\n", "\n\t\t")))

    # Show
    if verbose > 5:
        print("\nweights={0} | threshold={1}".format(weights, threshold))
        print(aux)

    # Extract vectors
    wgn = aux.W_GENUS
    wsp = aux.W_SPECIE
    sari = aux.RESISTANCE
    th = aux.THRESHOLD

    # Compute score
    score = np.sum(wgn * wsp * (sari <= th))

    # Create results
    d = {'N_GENUS': aux.GENUS.nunique(),
         'N_SPECIE': aux.SPECIE.nunique(),
         'ASAI_SCORE': score}

    # Default weights
    return pd.Series(d)




class ASAI():
  """This class computes the antimicrobial spectrum of activity. 

  The antimicrobial spectrum of activity (ASAI) represents ....

  The mathematical definition is...

  An example is to compute the ASAI for gram-positive and gram-negative
  bacteria. In that example, the ASAI indicates whether or not 
  the antimicrobial is effective against (i) different grams (n/p) which 
  is often denoted as broad spectrum (ii) different species within the
  same gram often denoted as intermediate spectrum or (iii) a particular
  species in a particular gram often denoted as narrow spectrum.

  input.csv ::

    id,gram,specie,genus,antibiotic,resistance
    1,p,specie1,genusa,antibiotic1,8
    2,p,specie1,genusb,antibiotic1,10
    3,p,specie1,genusc,antibiotic1,50
    4,p,specie2,genusa,antibiotic1,20
    5,p,specie3,genusa,aantibiotic1,50

  output.csv ::

    antibiotic, gramn, gramp.
    antibiotic1, NaN, 5.6667
    antibiotic2, 1.0, 1.0000
    antibiotic3, NaN, 5.6667

  .. todo::

    Add an example (executable)

  """
  # Attributes
  c_abx = 'ANTIBIOTIC'
  c_gen = 'GENUS'
  c_spe = 'SPECIE'
  c_res = 'RESISTANCE'
  c_thr = 'THRESHOLD'
  c_fre = 'FREQUENCY'
  c_wgen = 'W_GENUS'
  c_wspe = 'W_SPECIE'


  def __init__(self, weights='uniform', threshold=0.5,
                                        column_genus=c_gen, 
                                        column_specie=c_spe, 
                                        column_antibiotic=c_abx,
                                        column_resistance=c_res,
                                        column_threshold=c_thr,
                                        column_frequency=c_fre,
                                        column_wgenus=c_wgen,
                                        column_wspecie=c_wspe):
    """The constructor.

    Parameters
    ----------
    threshold : number
      The threshold under which the drug is considered effective.

    weights : string
      The method to compute the weights

    column_genus : string
      The column name with the genus values

    column_specie : string
      The column name with the specie values
    
    column_antibiotic : string 
      The column name with the antibiotic values
    
    column_resistance : string
      The column name with the resistance values
    
    column_threshold : string
      The column name with the threshold values
    
    column_frequency : string
      The column name with the frequency values
    
    Returns
    -------
    none
    """
    # Set parameters
    self.weights = weights
    self.threshold = threshold

    # Create dictionary to rename columns
    self.rename_columns = {column_genus: self.c_gen,
                           column_specie: self.c_spe,
                           column_antibiotic: self.c_abx,
                           column_resistance: self.c_res,
                           column_threshold: self.c_thr,
                           column_frequency: self.c_fre,
                           column_wgenus: self.c_wgen,
                           column_wspecie: self.c_wspe}

    # Columns that are required
    self.required_columns = [self.c_gen, self.c_spe, self.c_abx, self.c_res]


  def compute(self, dataframe, by_category):
    """This function computes the asai index by category.

    Parameters
    ----------
    dataframe : pandas DataFrame
      The pandas DataFrame containing the data. In particular it needs to
      contain the following columns: genus, specie, antibiotic and the
      resistance outcome within the range [0,1].

    by_category : string
      The name of the column that will be used to group ASAI.

    Returns
    -------
    pandas dataframe
      the dataframe...
    """
    # Check that it is a dataframe
    if not isinstance(dataframe, pd.DataFrame):
      raise TypeError("The instance passed as argument needs to be a pandas "
                      "DataFrame. Instead, a <%s> was found. Please convert "
                      "the input accordingly." % type(dataframe))

    # Rename columns
    dataframe = dataframe.rename(columns=self.rename_columns, copy=True)

    # Check dataframe columns
    _check_asai_dataframe_columns(dataframe, self.required_columns)

    # Check that there are no duplicates
    dataframe = dataframe.drop_duplicates(subset=[self.c_gen, 
                                                  self.c_spe, 
                                                  self.c_abx, 
                                                  by_category])

    # Check that no intrinsic resistance is considered
    dataframe = dataframe[dataframe[self.c_res]!=1.0]

    # Check that the by parameter has all value different than none
    dataframe = dataframe.dropna(subset=[by_category])

    # Compute asai and return
    return dataframe.groupby(by=[self.c_abx, by_category]) \
                    .apply(_asai, threshold=self.threshold) \
                    .unstack()





if __name__ == '__main__':
  

  # Import libraries
  import sys
  import numpy as np
  import seaborn as sns
  import matplotlib as mpl
  import matplotlib.pyplot as plt

  # Import specific libraries
  from pyamr.datasets import load

  # Configure seaborn style (context=talk)
  sns.set(style="white")

  # Set matplotlib
  mpl.rcParams['xtick.labelsize'] = 9
  mpl.rcParams['ytick.labelsize'] = 9
  mpl.rcParams['axes.titlesize'] = 11
  mpl.rcParams['legend.fontsize'] = 9

  # Pandas configuration
  pd.set_option('display.max_colwidth', 40)
  pd.set_option('display.width', 300)
  pd.set_option('display.precision', 4)

  # Numpy configuration
  np.set_printoptions(precision=2)


  # ---------------------
  # helper method
  # ---------------------
  def scalar_colormap(values, cmap, vmin, vmax):
    """This method creates a colormap based on values.

    Parameters
    ----------
    values : array-like
      The values to create the corresponding colors

    cmap : str
      The colormap

    vmin, vmax : float
      The minimum and maximum possible values

    Returns
    -------
    scalar colormap
    """
    # Create scalar mappable
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    # Gete color map
    colormap = sns.color_palette([mapper.to_rgba(i) for i in values])
    # Return
    return colormap


  # ---------------------
  # Create data
  # ---------------------
  # Create data
  data = [['GENUS_1', 'SPECIE_1', 'ANTIBIOTIC_1', 'N', 0.6000, 0.05],
          ['GENUS_2', 'SPECIE_2', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
          ['GENUS_2', 'SPECIE_3', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
          ['GENUS_2', 'SPECIE_4', 'ANTIBIOTIC_1', 'N', 0.0064, 0.05],
          ['GENUS_2', 'SPECIE_5', 'ANTIBIOTIC_1', 'N', 0.0073, 0.05],
          ['GENUS_2', 'SPECIE_6', 'ANTIBIOTIC_1', 'N', 0.0056, 0.05],
          ['GENUS_3', 'SPECIE_7', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
          ['GENUS_4', 'SPECIE_8', 'ANTIBIOTIC_1', 'N', 0.0518, 0.05],
          ['GENUS_4', 'SPECIE_9', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
          ['GENUS_4', 'SPECIE_10', 'ANTIBIOTIC_1', 'N', 0.0595, 0.05],
          
          ['GENUS_1', 'SPECIE_1', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_2', 'SPECIE_2', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_2', 'SPECIE_3', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_2', 'SPECIE_4', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_2', 'SPECIE_5', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_2', 'SPECIE_6', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_3', 'SPECIE_7', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_4', 'SPECIE_8', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_4', 'SPECIE_9', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
          ['GENUS_5', 'SPECIE_10', 'ANTIBIOTIC_1', 'P', 0.0, 0.05]]

  # Create dataframe
  dataframe = pd.DataFrame(data, columns=['GENUS', 
                                          'SPECIE', 
                                          'ANTIBIOTIC',
                                          'GRAM',
                                          'RESISTANCE',
                                          'THRESHOLD'])

  # -------------------------------
  # Create antimicrobial spectrum
  # -------------------------------
  # Create antimicrobial spectrum of activity instance
  asai = ASAI(weights='uniform', threshold=0.05,
                                 column_genus='GENUS',
                                 column_specie='SPECIE', 
                                 column_antibiotic='ANTIBIOTIC', 
                                 column_resistance='RESISTANCE',
                                 column_threshold='THRESHOLD')

  # Compute
  scores = asai.compute(dataframe, by_category='GRAM')

  # Show
  print(scores)

  # -----------------------------
  # Plot
  # ----------------------------- 
  # Variables to plot.
  x = scores.index.values
  y_n = scores['ASAI_SCORE']['N'].values
  y_p = scores['ASAI_SCORE']['P'].values

  # Constants
  colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
  colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

  # Create figure
  f, ax = plt.subplots(1, 1, figsize=(8, 0.5))

  # Plot
  sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h', 
    saturation=0.5, label='Gram-positive')
  sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h', 
    saturation=0.5, label='Gram-negative')

  # Configure
  sns.despine(bottom=True)

  # Configure
  ax.set_xlim([-1,1])

  # Legend
  plt.legend()

  # Display
  plt.show()