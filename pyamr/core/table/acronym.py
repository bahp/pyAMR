###############################################################################
# Author: Bernard Hernandez
# Filename: acronym.py
# Date: 02/09/2015
# Description:
# 
# This script creates a map to solve possible issues of misspelled antibiotics,
# or differences as upper/lower cases, unnecessary spaces, missing codes, ...
# Hence, it creates a conversion between the original antibiotic name to an
# homogenous antibiotic name, and the original code and an homogeneous code.
#
###############################################################################

# Libraries
import pandas as pd

# --------------------------------------------------------------------------
#                              helper methods
# --------------------------------------------------------------------------
def acronym(name, length=3, prefix='A_'):
  """This method created the acronym for a given string

  Parameters
  ----------
  name: string-like
    The string to construct the acronym

  length: int-like
    The number of letters used for the first word of the acronym

  prefix: string-like
    The prefix to add to the acronym for identification purposes

  Returns
  -------
  string
  """
  # Check that the acronym is not nul
  # Remove spaces
  name = ' '.join(name.split())
  # Array with individual words
  words = name.split()   
  # Check there are words to create acronym
  if not len(words):
    return ('%sNONE' % (prefix)).upper()
  # Create acronym for other words
  acronym = [w[0] for w in words[1:]]
  # Create acronym adding first word
  acronym = '%s%s%s' % (prefix, words[0][:length], ''.join(acronym))
  # Return
  return acronym.upper()


def _check_acronym_conflicts(transdict):
  """This method check that all acronyms are unique.

  Parameters
  ----------
  transdict: dict-like
    The dictionar containing the string and the corresponding acronym.

  Returns
  -------
  """
  # Import library
  from collections import Counter
  # Count number of times the acronym appears
  counter = Counter(transdict.values())
  # Create a dict with the duplicated elements
  duplicated = {k:v for k,v in counter.items() if v>1}
  # Raise an error
  if len(duplicated):
    raise ValueError("The following acronyms within the dictionary "
                     "are not unique %s." % duplicated)


class AcronymBuilder:
  """
  """

  # Attributes
  _func = acronym

  # Constructor
  def __init__(self):
    """
    """
    pass
  
  def has_acronym():
    pass

  def has_value():
    pass

  def update(self):
    pass

  def fit(self, values, acronyms):
    """This method creates a dictionary with the acronyms

    TODO: Instead of just checking whether there are acronym conflicts or not
    ensure that always unique acronyms are created. Note that the implemented
    approach to create acronyms does not ensure they are always unique.

    Parameters
    ----------
    values: array-like (contains strings)
      The array with the possible values

    acronyms: array-like (contains strings)
      The array with the corresponding acronyms.

    Returns
    -------
    """
    # Check that lengths are the same
    if len(values)!=len(acronyms):
      raise ValueError("The length of the parameters values (%s) and "
                       "acronyms (%s) mismatch. They must be the same "
                       "length." % (len(values), len(acronyms)))

    # Remove duplicated spaces within values
    values = [' '.join(v.split()).lower() for v in values]

    # Create acronyms for nan entries
    acronyms = [acronym(v) if pd.isnull(a) else a 
      for v,a in zip(values, acronyms)]

    # Create translation dictionary
    self._transdict = dict(zip(values, acronyms))
    self._reverdict = dict(zip(acronyms, values))

    # Check acronym conflicts
    _check_acronym_conflicts(self._transdict)
    _check_acronym_conflicts(self._reverdict)

    # Return
    return self


  def transform(self, values):
    """This method returns the acronyms for given values

    Parameters
    ----------
    values: array-like

    Returns
    -------
    array with acronyms
    """
    return [self._transdict[value] for value in values]

  def inverse_transform(self, acronyms):
    """This method returns the values for given acronyms.

    Parameters
    ----------
    values: array-like

    Returns
    -------
    array with acronyms
    """
    return [self._reverdict[acronym] for acronym in acronyms]

  












if __name__ == '__main__':

  # Libraries
  import sys

  # Import specific libraries
  from pyamr.datasets import load


  # ---------------------
  # Example I
  # ---------------------
  # This example shows how to use the acronym builder to generate acronyms
  # to be used for the EPiC IMPOC research. In particular, it creates the
  # acronyms for the organisms.

  # Load data
  data = load.dataset_epicimpoc_susceptibility_year()
  data = data[['organismNameOrig', 'organismCodeOrig']].drop_duplicates()

  # Create the acronym builder
  builder = AcronymBuilder()

  # Get values and acronyms
  values = data['organismNameOrig'].values
  acronyms = data['organismCodeOrig'].values

  print(pd.DataFrame(values, acronyms))

  # Fit builder
  builder.fit(values=values, acronyms=acronyms)

  # Transform
  print(builder.transform(['enterococcus sp.', 'pseudomonas sp.']))

  # Inverse transform
  print(builder.inverse_transform(['ENTC', 'PSEUD']))


  # ---------------------
  # Example II
  # ---------------------
  # This example shows how the existing acronym generation approach 
  # fails for the terms 'feo guapo' and 'feo gordo' which produce the 
  # same acronym.
  # Create data
  a = ''
  b = 'feo'
  c = 'feo   guapo'
  d = 'feo guapo tonto'
  e = 'feo gordo'

  # Create the acronym builder
  builder = AcronymBuilder()

  # Get values and acronyms
  values = [a, b, c, d, e]
  acronyms = [acronym(name) for name in values]

  # Fit builder
  builder.fit(values=values, acronyms=acronyms)
