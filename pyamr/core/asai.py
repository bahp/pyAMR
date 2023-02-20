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
def _check_asai_weights_genus(dataframe): # pragma: no cover
  """Checks that the weights for each genus add up to one.

  .. deprecated:: 0.0.1

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


def _check_asai_weights_specie(dataframe): # pragma: no cover
  """Check that the weights for all the species add up to one.

  .. deprecated:: 0.0.1

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


def _check_asai_dataframe_columns(dataframe, required_columns): # pragma: no cover
  """This method checks that the dataframe has all attributes.

  .. deprecated:: 0.0.1

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


def _asai(dataframe, threshold=None, weights='uniform'): # pragma: no cover
  """Computes the antimicrobial spectrum of activity.

  .. deprecated:: 0.0.1

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


def _asai_score(weights_genus, weights_specie, resistance, threshold): # pragma: no cover
  """Computes the asai score.

  .. deprecated:: 0.0.1

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



def asai(dataframe, weights='uniform', threshold=0.5, tol=1e-6, verbose=0):
    """Computes the ASAI.

    .. note: Since threshold and weights have a default value, the
             warnings below will not be displayed. However, the code
             is there in case the behaviour needs to be changed in
             the future.

    .. note: Another way to check that the weights are correct is just
             by computing ASAI with th=0 and th=1. These should result
             in asai=1 and asai=0 respectively.

                 # Compute score
                 score_1 = np.sum(wgn * wsp * (sari <= 0))
                 score_2 = np.sum(wgn * wsp * (sari <= 1))


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
        [W_GENUS and W_SPECIE] are required if weights is None. Also,
        if weights = 'frequency' the column FREQUENCY must be present.

    weights: string, default='frequency'
        The method to compute the weights. The methods supported are:

            - 'specified': weights must be specified in [W_GENUS and W_SPECIE]
            - 'uniform': uniform weights for genus and species within genus.
            - 'frequency': weights are proportional to the frequencies.

        The following rules must be fulfilled by the weight columns:

            - consistent weight for a given genus
            - all genus weights must add up to one.
            - all specie weights within a genus must add up to one.

    threshold: float, default=None
        The threshold resistance value above which the antimicrobial is
        considered non-effective to treat the microorganism. For instance,
        for a resistance threshold of 0.5, if a pair <o,a> has a resistance
        value of 0.4, the microorganism will be considered sensitive. In
        order to use specific thresholds keep threshold to None and include
        a column 'THRESHOLD'.ss

    tol: float, default=1e-6
        The tolerance in order to check that all conditions (uniqueness
        and sums) are satisfied. Note that that float precision varies
        and therefore not always adds up to exactly one.

    verbose: int, default=0
        The level of verbosity.

    Returns
    -------
    pd.DataFrame
        The dataframe with the ASAI information and counts.
    """
    # Required columns
    required = ['RESISTANCE', 'GENUS', 'SPECIE']

    # Add weight-related required columns
    if weights == 'specified':
        required += ['W_GENUS', 'W_SPECIE']
    if weights == 'frequency':
        required += ['FREQUENCY']

    # Check weights
    if weights not in ['uniform', 'frequency', 'specified']:
        raise ValueError("""
              The weights '{0}' is not supported. Please
              use one of the following: uniform, frequency
              or specified""".format(weights))

    # Bad input type
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("""\n
            The instance passed as argument needs to be a pandas 
            "DataFrame. Instead, a <%s> was found. Please convert 
            the input accordingly.""" % type(dataframe))

    # Check columns
    if set(required).difference(dataframe.columns):
        raise ValueError("The following columns are missing: {0} " \
                .format(set(required).difference(dataframe.columns)))

    # Check duplicates
    if dataframe.duplicated().any():
        raise ValueError("There are duplicated rows in the DataFrame.")

    # Get NaN idxs
    idxs = dataframe[required].isna().any(axis=1)

    # Show warning and correct
    if idxs.any():
        raise ValueError("""\n
              There are NULL values in columns that are required.
              Please correct this issue and try again. See below 
              for more information:\n\n\t\t{0}""".format(
                dataframe.loc[idxs, required] \
                    .to_string().replace("\n", "\n\t\t")
        ))

    # Copy DataFrame
    aux = dataframe.copy(deep=True)

    # Check threshold
    if 'THRESHOLD' in aux.columns:
        if threshold is not None:
            warnings.warn("""\n
                  The threshold has been defined both as an 
                  input parameter (threshold={0}) and a DataFrame 
                  column 'THRESHOLD'. The latter will be used."""
                  .format(threshold))
    else:
        if threshold is None:
            warnings.warn("""\n
                  The threshold has not been defined using either 
                  an input parameter (threshold={0}) or a column in the 
                  dataframe named 'THRESHOLD'. Thus a default threshold 
                  value of '0.5' will be used.""".format(threshold))
            threshold = 0.5
        aux['THRESHOLD'] = threshold

    # Set uniform weights
    if weights == 'uniform':
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
    #report = pd.DataFrame()
    #report['W_GENUS_UNIQUE_OK'] = aux.groupby('GENUS').W_GENUS.nunique()
    #report['W_GENUS_SUM_OK'] = aux.groupby('GENUS').head(1).W_GENUS.sum()
    #report['W_SPECIE_SUM_OK'] = aux.groupby(['GENUS']).W_SPECIE.sum()

    #if verbose > 5:
    #    # Explain each error individually.
    #    pass

    # Condition
    #condition = (1 - report).abs() < tol

    # Report
    #if not condition.all().all():
    #    raise ValueError("""
    #        The weights imputed do not fulfill all the requirements. Please
    #        check the report below and correct the weights accordingly. Note
    #        a given genus must have a consistent weight and the sum of weights
    #        must add up to 1.\n\n\t\t{0}""" \
    #        .format(condition.to_string().replace("\n", "\n\t\t")))

    # Show
    if verbose > 5:
        print("\nweights={0} | threshold={1}".format(weights, threshold))
        print(aux)

    # Extract vectors
    wgn = aux.W_GENUS
    wsp = aux.W_SPECIE
    sari = aux.RESISTANCE
    th = aux.THRESHOLD

    # Check range using extreme thresholds
    s1 = np.sum(wgn * wsp * (sari < 0))
    s2 = np.sum(wgn * wsp * (sari <= 1))
    if abs(s1-0) > tol or abs(s2-1) > tol:
        raise ValueError("""
            The weights argument do not fulfill all the requirements. Note
            that the correct weights would produce a SARI value within the
            range [0, 1]. However, the weights received did not fulfill 
            such constraint.""")

    # Compute score
    score = np.sum(wgn * wsp * (sari < th))

    # Create results
    d = {
        'N_GENUS': aux.GENUS.nunique(),
        'N_SPECIE': aux.SPECIE.nunique(),
        'ASAI_SCORE': score
    }

    # Default weights
    return pd.Series(d)







class ASAI():

    # Attributes
    c_gen = 'GENUS'
    c_spe = 'SPECIE'
    c_res = 'RESISTANCE'
    c_thr = 'THRESHOLD'
    c_fre = 'FREQUENCY'
    c_wgen = 'W_GENUS'
    c_wspe = 'W_SPECIE'

    def __init__(self, column_genus=c_gen,
                       column_specie=c_spe,
                       column_resistance=c_res,
                       column_threshold=c_thr,
                       column_frequency=c_fre,
                       column_wgenus=c_wgen,
                       column_wspecie=c_wspe):
        """The constructor.

        Parameters
        ----------
        column_genus: string
            The column name with the genus values

        column_specie: string
            The column name with the specie values

        column_resistance: string
            The column name with the resistance values

        column_threshold: string
            The column name with the threshold values

        column_frequency: string
            The column name with the frequency values

        Returns
        -------
        none
        """
        # Create dictionary to rename columns
        self.rename = {column_genus: self.c_gen,
                       column_specie: self.c_spe,
                       column_resistance: self.c_res,
                       column_threshold: self.c_thr,
                       column_frequency: self.c_fre,
                       column_wgenus: self.c_wgen,
                       column_wspecie: self.c_wspe}

        # Columns that are required
        self.required = [self.c_gen, self.c_spe, self.c_res]


    def compute(self, dataframe, groupby=None, min_freq=None, **kwargs):
        """Computes the ASAI index (safely).

        .. note: Review first NaN and then duplicated?
        .. note: Review extreme values in resistance?

        Parameters
        ----------
        dataframe: pd.DataFrame
            The pandas dataframe with the information. The following columns
            are always required [RESISTANCE, GENUS and SPECIE]. In addition,
            [W_GENUS and W_SPECIE] are required if weights is None. Also,
            if weights = 'frequency' the column FREQUENCY must be present.

        groupby: list, default=None
            The elements to groupby (pd.groupby)

        min_freq: int, default=None
            The minimum number of susceptibility tests required in order to
            include the species to compute ASAI. Note that to work the dataframe
            must include a column indicating the frequencies.

        weights: string, default=None
            The method to compute the weights. The methods supported are:

                - None: weights must be specified in [W_GENUS and W_SPECIE]
                - 'uniform': uniform weights for genus and species within genus.
                - 'frequency: weights are proportional to the frequencies.

            The following rules must be fulfilled by the weight columns:

                - consistent weight for a given genus
                - all genus weights must add up to one.
                - all specie weights within a genus must add up to one.

        threshold: float, default=None
            The threshold resistance value above which the antimicrobial is
            considered non-effective to treat the microorganism. For instance,
            for a resistance threshold of 0.5, if a pair <o,a> has a resistance
            value of 0.4, the microorganism will be considered sensitive. In
            order to use specific thresholds keep threshold to None and include
            a column 'THRESHOLD'.ss

        tol: float, default=1e-6
            The tolerance in order to check that all conditions (uniqueness
            and sums) are satisfied. Note that that float precision varies
            and therefore not always adds up to exactly one.

        verbose: int, default=0
            The level of verbosity.

        Returns
        -------
        pd.DataFrame
            The dataframe with the ASAI information and counts.
        """
        # Bad input type
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("""
                The instance passed as argument needs to be a pandas
                DataFrame. Instead, a <%s> was found. Please convert 
                the input accordingly.""" % type(dataframe))

        if isinstance(groupby, str):
            groupby = [groupby]

        # Create auxiliary variable
        required = groupby + self.required

        # Rename columns
        aux = dataframe.rename(columns=self.rename, copy=True)

        # Filter by freq
        if min_freq is not None:
            if not self.c_fre in aux:
                warnings.warn("""
                The min_freq={0} cannot be applied because the frequency
                columns 'FREQUENCY' does not exist in the DataFrame.\n"""
                    .format(min_freq))
            else:
                aux = aux[aux[self.c_fre] >= min_freq]


        # Check duplicates
        if aux.duplicated(subset=required).any():
            warnings.warn("""
                 There are duplicated rows in the DataFrame. This is
                 usually not expected. Please review the DataFrame and 
                 address this inconsistencies. Maybe you should include
                 more columns in the groupby (e.g. specimen_code). The 
                 columns used to compute duplicated are: 
                 {0}.\n""".format(required))
            #aux = aux.drop_duplicates(required)

        # Check extreme resistance values
        if aux.RESISTANCE.isin([0.0, 1.0]).any():
            warnings.warn("""
                 Extreme resistances [0, 1] were found in the DataFrame. These 
                 rows should be reviewed since these resistances might correspond
                 to pairs with low number of records.\n""")
            #aux = aux[aux[self.c_res] != 1.0]

        # Get NaN indexes
        idxs = aux[required].isna().any(axis=1)

        # Show warning and correct
        if idxs.any():
            warnings.warn("""
                 There are NULL values in columns that are required. These
                 rows will be ignored to safely compute ASAI. Please review
                 the DataFrame and address this inconsistencies. See below
                 for more information: \n\n\t\t\t{0}\n""".format( \
                    aux[required].isna().sum(axis=0) \
                        .to_string().replace("\n", "\n\t\t\t")))
            aux = aux.dropna(subset=required)

        # Check all genus weights add up to one?

        # Compute
        scores = aux.groupby(groupby) \
                    .apply(asai, **kwargs)

        # Return
        return scores








class ASAI_old(): # pragma: no cover
  """This class computes the antimicrobial spectrum of activity. 

  .. deprecated:: 0.0.1

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





if __name__ == '__main__': # pragma: no cover

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
  data = [['GENUS_1', 'SPECIE_1', 'ANTIBIOTIC_1', 'N', 1, 0.6000, 0.05],
          ['GENUS_2', 'SPECIE_2', 'ANTIBIOTIC_1', 'N', 1, 0.0000, 0.05],
          ['GENUS_2', 'SPECIE_3', 'ANTIBIOTIC_1', 'N', 1, 0.0000, 0.05],
          ['GENUS_2', 'SPECIE_4', 'ANTIBIOTIC_1', 'N', 1, 0.0064, 0.05],
          ['GENUS_2', 'SPECIE_5', 'ANTIBIOTIC_1', 'N', 1, 0.0073, 0.05],
          ['GENUS_2', 'SPECIE_6', 'ANTIBIOTIC_1', 'N', 1, 0.0056, 0.05],
          ['GENUS_3', 'SPECIE_7', 'ANTIBIOTIC_1', 'N', 1, 0.0000, 0.05],
          ['GENUS_4', 'SPECIE_8', 'ANTIBIOTIC_1', 'N', 1, 0.0518, 0.05],
          ['GENUS_4', 'SPECIE_9', 'ANTIBIOTIC_1', 'N', 1, 0.0000, 0.05],
          ['GENUS_4', 'SPECIE_10', 'ANTIBIOTIC_1', 'N', 1, 0.0595, 0.05],
          
          ['GENUS_1', 'SPECIE_1', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_2', 'SPECIE_2', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_2', 'SPECIE_3', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_2', 'SPECIE_4', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_2', 'SPECIE_5', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_2', 'SPECIE_6', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_3', 'SPECIE_7', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_4', 'SPECIE_8', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_4', 'SPECIE_9', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05],
          ['GENUS_5', 'SPECIE_10', 'ANTIBIOTIC_1', 'P', 1, 0.0, 0.05]]

  # Create dataframe
  dataframe = pd.DataFrame(data, columns=['GENUS', 
                                          'SPECIE', 
                                          'ANTIBIOTIC',
                                          'GRAM',
                                          'FREQUENCY',
                                          'RESISTANCE',
                                          'THRESHOLD'])

  print(dataframe)

  # -------------------------------
  # Create antimicrobial spectrum
  # -------------------------------
  # Create antimicrobial spectrum of activity instance
  obj = ASAI(column_genus='GENUS',
             column_specie='SPECIE',
             column_resistance='RESISTANCE',
             column_frequency='FREQUENCY',
             column_threshold='THRESHOLD',
             column_wgenus='W_GENUS',
             column_wspecie='W_SPECIE')

  # Compute
  scores = obj.compute(dataframe,
    groupby=['ANTIBIOTIC', 'GRAM'],
    weights='frequency',
    threshold=0.5,
    min_freq=0)

  # Unstack
  scores = scores.unstack()

  # Show
  print("\nResults:")
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
  #plt.show()


  # -------------------------------------------------------------------------
  # Testing
  # -------------------------------------------------------------------------
  # Create data
  data = [['STAPH', 'COAGU', 'ANTIBIOTIC_1', 'P', 0.88, 1, 0.20, 1 / 10, 1 / 3],
          ['STAPH', 'EPIDE', 'ANTIBIOTIC_1', 'P', 0.11, 1, 0.20, 1 / 10, 1 / 3],
          ['STAPH', 'HAEMO', 'ANTIBIOTIC_1', 'P', 0.32, 1, 0.20, 1 / 10, 1 / 3],
          ['STAPH', 'LUGDU', 'ANTIBIOTIC_1', 'P', 0.45, 1, 0.20, 1 / 10, 1 / 3],
          ['STAPH', 'SAPRO', 'ANTIBIOTIC_1', 'P', 0.18, 1, 0.20, 1 / 10, 1 / 3],
          ['STAPH', 'AUREU', 'ANTIBIOTIC_1', 'P', 0.13, 5, 0.20, 5 / 10, 1 / 3],

          ['ENTER', 'DURAN', 'ANTIBIOTIC_1', 'N', 0.64, 1, 0.20, 1 / 4, 1 / 3],
          ['ENTER', 'FAECI', 'ANTIBIOTIC_1', 'N', 0.48, 1, 0.20, 1 / 4, 1 / 3],
          ['ENTER', 'GALLI', 'ANTIBIOTIC_1', 'N', 0.10, 1, 0.20, 1 / 4, 1 / 3],
          ['ENTER', 'FAECA', 'ANTIBIOTIC_1', 'N', 0.09, 1, 0.20, 1 / 4, 1 / 3],

          ['STREP', 'VIRID', 'ANTIBIOTIC_1', 'P', 0.08, 1, 0.20, 1 / 3, 1 / 3],
          ['STREP', 'PNEUM', 'ANTIBIOTIC_1', 'P', 0.89, 2, 0.20, 2 / 3, 1 / 3]]

  # Create dataframe
  dataframe = pd.DataFrame(data, columns=['GENUS',
                                          'SPECIE',
                                          'ANTIBIOTIC',
                                          'GRAM',
                                          'RESISTANCE',
                                          'FREQUENCY',
                                          'THRESHOLD',
                                          'W_SPECIE',
                                          'W_GENUS'])


  # ---------------------------------------------------------------------
  # Success
  # ---------------------------------------------------------------------
  # .. note: All this examples should succeed. At the moment the code
  #          breaks if gram is not included. This is because the data
  #          we have created has duplicated values for each gram.
  #          Should we consider this within the ASAI?
  cols = ['GENUS',
          'SPECIE',
          'ANTIBIOTIC',
          'RESISTANCE',
          'GRAM']

  def show_i(i, df):
      print("\n\n%s:" % i)
      print(df)

  # Using minimum number of columns
  r = dataframe[cols]\
      .groupby(['ANTIBIOTIC', 'GRAM']) \
      .apply(asai, weights='uniform',
                   threshold=0.5)
  show_i("Using minimum number of columns", r)

  # User defined constant threshold
  r = dataframe[cols]\
      .groupby(['ANTIBIOTIC', 'GRAM']) \
      .apply(asai, weights='uniform',
                   threshold=0.05)
  show_i("User defined constant threshold", r)

  # Use frequency to compute weights
  r = dataframe[cols + ['FREQUENCY']] \
      .groupby(['ANTIBIOTIC']) \
      .apply(asai, weights='frequency',
                   threshold=0.05)
  show_i("Use frequency to compute weights", r)

  # Use weights previously specified.
  r = dataframe[cols + ['W_GENUS', 'W_SPECIE']] \
      .groupby(['ANTIBIOTIC']) \
      .apply(asai, weights='specified',
                   threshold=0.05)
  show_i("Use weights specified manually", r)


  # ---------------------------------------------------------------------
  # ASAI - Errors
  # ---------------------------------------------------------------------
  # .. note: In the examples below, the method asai is meant to raise
  #          an error either because any of the required missing columns
  #          is missing or because the weight configuration is not
  #          correct.
  print("\n\nHandling errors:")

  try:
      # Error: resistance column is missing
      r = dataframe.drop(columns=['RESISTANCE']) \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai)
  except Exception as e:
      print(e)

  try:
      # Error: genus column is missing
      r = dataframe.drop(columns=['GENUS']) \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai)
  except Exception as e:
      print(e)

  try:
      # Error: specie column is missing
      r = dataframe.drop(columns=['SPECIE']) \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai)
  except Exception as e:
      print(e)

  try:
      # Error: w_genus and/or w_specie columns are missing
      r = dataframe.drop(columns=['W_GENUS', 'W_SPECIE'])  \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai, weights='specified')
  except Exception as e:
      print(e)

  try:
      # Error: weights is not a valid value
      r = dataframe  \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai, weights=None)
  except Exception as e:
      print(e)

  try:
      # Error: weights not valid (W_GENUS)
      aux = dataframe.copy(deep=True)
      aux.loc[0, 'W_GENUS'] = 1
      r = aux \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai, weights='specified')
  except Exception as e:
      print(e)

  try:
      # Error: weights not valid (W_SPECIE)
      aux = dataframe.copy(deep=True)
      aux.loc[0, 'W_SPECIE'] = 1
      r = aux \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai, weights='specified')
  except Exception as e:
      print(e)

  try:
      # Error: null values in required column
      aux = dataframe.copy(deep=True)
      aux.loc[0, 'RESISTANCE'] = np.NaN
      r = aux \
          .groupby(['ANTIBIOTIC']) \
          .apply(asai)
  except Exception as e:
      print(e)





  # ---------------------------------------------------------------------
  # ASAI - Warnings
  # ---------------------------------------------------------------------
  # .. note: In the examples below, the method asai is meant to show a
  #          warning message either no threshold has been specified or
  #          because thresholds have been specified twice.
  print("\n\nShow warnings:")

  # Warning: default threshold=0.5 and THRESHOLD column passed.
  r = dataframe \
      .groupby(['ANTIBIOTIC', 'GRAM']) \
      .apply(asai)

  # Warning: threshold is None and no column THRESHOLD
  r = dataframe.drop(columns=['THRESHOLD']) \
      .groupby(['ANTIBIOTIC']) \
      .apply(asai, threshold=None)

