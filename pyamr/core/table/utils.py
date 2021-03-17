###############################################################################
# Author: Bernard Hernandez
# Filename: generic.py
# Date: 02/09/2015
# Description: Methods to clean data.
#
###############################################################################

# Libraries.
from os import listdir
import numpy as np
import pandas as pd
import datetime
import glob
import json
import re

#-------------------------------------------------------------------------
#                         generic functions
#-------------------------------------------------------------------------
def _apply(df, cols, fun):
  """
  """
  if isinstance(cols, str): 
    cols = df.columns if cols=='all' else [cols]
  for col in cols:
    if col in df.columns:
      df[col] = df[col].apply(fun)
  return df

def _lower(x):
  """This method lowers the string"""
  try: 
    return x.lower()
  except: 
    return x

def _upper(x):
  """This method uppers the string"""
  try: 
    return x.upper()
  except: 
    return x

def _delete_spaces(x):
  """
  """
  try: 
    return ' '.join(x.split())
  except: 
    return x

def _delete_digits(x):
  """
  """
  try: 
    return ''.join([i for i in x if not i.isdigit()])
  except: 
    return x

def _delete_types(x):
  """
  """
  try:
    if not isinstance(x, str): return x
    if '(second type)' in x: return x.replace(' (second type)', '')
    if '(2nd type)' in x: return x.replace(' (2nd type)', '')
    if '(third type)' in x: return x.replace(' (third type)', '')
    if '(3rd type)' in x: return x.replace(' (3rd type)', '')
    return x
  except Exception as e:
    print e
    return x

def _delete_parenthesis_content(x):
  """
  """
  try:
    if not isinstance(x, str): return x
    if re.search(r'\([^)]*\)',x) is not None:
      x = re.sub(r'\([^)]*\)', '', x)
      return _delete_spaces(x)
    return x
  except Exception as e:
    return x

def _fix_sp_ending(x):
  """
  """
  try:
    if not isinstance(x, str): return x
    if x.endswith('sp'): return x+'.'
    if x.endswith('sp..'): return x[:-1]
    if ' sp ' in x: return x.replace(' sp ', ' sp. ')
    if 'species' in x: return x.replace('species','sp.')
    return x
  except Exception as e:
    print e
    return x

def _fix_sp_abbreviation(x):
  """
  """
  try:
    if not isinstance(x, str): return x
    if 'streptococci' in x: return x.replace('streptococci', 'streptococcus')
    if "strep." in x: return x.replace('strep.', 'streptococcus')
    if "staph." in x: return x.replace('staph.', 'staphylococcus ')
    return x
  except Exception as e:
    print e
    return x

#-------------------------------------------------------------------------
#                         GENERAL METHODS
#-------------------------------------------------------------------------
def lettercase(df, cols='all', funct=_lower):
  """
  """
  if isinstance(funct, str): 
    if funct=='lower': return _apply(df, cols, _lower)
    if funct=='upper': return _apply(df, cols, _upper)
  else:
    return _apply(df, cols, funct)

def delete_spaces(df, cols='all'):
  """
  """
  return _apply(df, cols, _delete_spaces)

def delete_parenthesis(df, cols='all'):
  """
  """
  return _apply(df, cols, _delete_parenthesis_content)

#-------------------------------------------------------------------------
#                      SENSITIVTY ORIENTED METHODS
#-------------------------------------------------------------------------
def delete_numbers(df, cols='all'):
  """
  """
  return _apply(df, cols, _delete_digits)

def delete_types(df, cols='all'):
  """
  """
  return _apply(df, cols, _delete_types)

def ending_specie(df, cols='all'):
  """
  """
  return _apply(df, cols, _fix_sp_ending)

def specie_abbreviation(df, cols='all'):
  """
  """
  return _apply(df, cols, _fix_sp_abbreviation)


# -----------------------------------------------------------
#
# -----------------------------------------------------------










def transform_rename(filepath, df):
  """This function rename codes (i.e. PAER1,PAER2 to PEAR)

  Parameters
  ----------

  Return
  ------
  """
  def transform_attribute(code_map, attr_name, df):
    """
    """
    for k in code_map:
      codes = code_map[k]
      is_in = df[attr_name].isin(codes)
      df.loc[is_in, attr_name] = k
    return df

  # Read config information.
  file = open(filepath) 
  config_info = json.load(file)
  print config_info
  # Variables.
  rename_drugs = config_info['drugs']['rename']
  rename_bugs = config_info['bugs']['rename']
  # Rename
  df = transform_attribute(rename_drugs, 'drugCode', df)
  df = transform_attribute(rename_bugs, 'organismCode', df)
  return df
  