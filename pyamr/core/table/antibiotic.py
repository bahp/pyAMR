###############################################################################
# Author: Bernard Hernandez
# Filename: antibiotics.py
# Date: 02/09/2015
# Description:
# 
# This script creates a map to solve possible issues of misspelled antibiotics,
# or differences as upper/lower cases, unnecessary spaces, missing codes, ...
# Hence, it creates a conversion between the original antibiotic name to an
# homogenous antibiotic name, and the original code and an homogeneous code.
#
###############################################################################

# Generic libraries.
import sys
import datetime
import numpy as np
import pandas as pd
import re

"""
# Own libraries.
sys.path.append('../../../../modules/')
import settings.organisms as ORG
import settings.antibiotics as ANT
import settings.microbiology as MBL
import others.io.read as pd_read
import others.clean.generic as pd_clean_gen
"""

# IMPORTANT
# =========
# Note that some of the constants used to indicate which columns should be
# lowercase, uppercase, ... are stated in the settings modules which can be
# found in modules/settings/antibiotics.py. In addition, the rename_map
# stores in modules/settings/microbiology.py should contain the mapping
# between the column names with the antibiotic name and code and the
# standard: antibioticNameOrig and antibioticCodeOrig



class AntibioticsTable:
  """
  """

  # ----------
  # Constants
  # ----------
  # Columns identifiers for the name and the code. Ensure that there is 
  # a conversion in the file modules/settings/microbiology.py from the
  # input data file column names to 'antibioticCodeOrig' and
  # 'ntibioticNameOrig'. The different letters indicate:
  # O - the original value that will be stored in the antibiotics table
  # F - the formated value that will be stored in the antibiotics table
  # P - the value of the column in the input data.
  nameO, codeO = 'antibioticNameOrig', 'antibioticCodeOrig'
  nameF, codeF = 'antibioticName', 'antibioticCode' 

  # The columns that should be read from the file. Note that the original
  # files are huge and might not be stored in memory. Therefore reducing
  # the columns kept in memory helps.
  usecols = [nameO, codeO] 

  # Length for automatic codes.
  l = 8

  # Constructor
  def __init__(self):
    txt = "Check that the columns with the ANTIBIOTIC name and code have "
    txt+= "mapped in the rename_map variable in the file "
    txt+= "module/settings/microbiology.py\n"
    print(txt)


  #------------------------------------------------------
  #                   PRIVATE METHODS
  #------------------------------------------------------
  def _acronym(self, words):
    """This method return the acronym of several words.
    """
    return "".join(e[0] for e in words)

  def _compute_main(self, name):
    """This method creates the main part of the code.
    """
    words = name.split(" ")
    if len(words)==1:   return name[:self.l]
    elif len(words)==2: return words[0][0]+words[1][:self.l]
    elif len(words)==3: return words[0][0]+words[1][0]+words[2][:self.l] 
    else:               return self._acronym(words)

  def _compute_automatic_code(self, row, l=8):
    """This method computes the automatic code (starting with A_). 
    """
    # Compute.
    main = self._compute_main(row[self.nameF])
    code = "A_%s" % main
    return code.upper()   

  def _compute_codes(self, df):
    """This method computes missing codes.
    """
    # compute codes
    for idx,elm in df.iterrows():
      # It already has a code.
      if not pd.isnull(elm[self.codeO]): continue
      # Needs an automatic code but name is empty.
      if pd.isnull(elm[self.nameO]): continue
      # Compute automatic code
      df.loc[idx, self.codeF] = self._compute_automatic_code(elm)
    # return
    return df



  #------------------------------------------------------
  #                  PUBLIC METHODS
  #------------------------------------------------------
  def merge_table(self, df1, df2, on, conflicts):
    """This function merges the two basic columns name and code.

    Parameters
    ----------
    df1 : the old dataframe with name and code.
    df2 : the new dataframe with name and code.

    Returns
    -------
    df_m : merged dataframe.
    df_c : conflicts dataframe.
    """
    # Merged dataframe
    df_m = pd.merge(df1, df2, on=on, how='outer')
    for c1 in df_m.columns[1:]:
      if not c1.endswith('_x') and not c1.endswith('_y'): continue
      c2 = c1[:-1]+'x' if c1.endswith('_y') else c1[:-1]+'y'
      df_m[c1].fillna(df_m[c2], inplace=True)
    # Find conflicts
    c1, c2 = conflicts+"_x", conflicts+"_y"
    df_c = df_m[df_m[c1]!=df_m[c2]]
    df_c = df_c[[on, c1, c2]]
    # Remove duplicated columns (y)
    for c in df_m.columns:
      if c.endswith('y'):
        del df_m[c]
    # Remove column names endings.
    for i,c in enumerate(df_m.columns.values):
      if c.endswith('x'):
        df_m.columns.values[i] = c[:-2]
    # Return
    return df_m, df_c


  def create_table(self, data_path):
    """This method creates the table from input data

    Parameters
    ----------

    Returns
    -------
    """

    # Read data.
    df = pd_read.read_data(ftype='csv', 
                           path=data_path, 
                           rename_map=MBL.rename_map,          # renaming cols
                           keep_cols=self.usecols,             # keep cols
                           std_cols=[self.nameO, self.codeO],  # std cols 
                           low_memory=False)
    # Unique combinations (NaN are not grouped so they are set to -1).
    df_u = df.replace(np.nan, "None")
    df_u = df_u.groupby([self.nameO, self.codeO]).size()
    df_u = df_u.reset_index().rename(columns={0:'count'})
    df_u = df_u.replace("None", np.nan)
    df_u[self.nameF] = df_u[self.nameO]
    df_u[self.codeF] = df_u[self.codeO]
    #df_u = df_u.reindex(columns=ANT.database_cols)
    del df_u['count']

    # Cleaning data (order matters).
    df_u = pd_clean_gen.lettercase(df_u, ANT.to_lowercase, 'lower')
    df_u = pd_clean_gen.lettercase(df_u, ANT.to_uppercase, 'upper')
    df_u = pd_clean_gen.delete_spaces(df_u, ANT.dl_spaces)
    df_u = pd_clean_gen.delete_parenthesis(df_u, ANT.dl_parenthesis)

    # Computing automatic codes.
    df_u = self._compute_codes(df_u)

    # Drop duplicates keeping the one in which the code is not NAN. For that
    # purpose we sort by values (therefore sending nans to the end) and then
    # use drop_duplicates() removing the last instance found.
    df_u = df_u.sort_values(by=self.codeO)
    df_u = df_u.drop_duplicates(subset=[self.nameO], keep='first')
    df_u = df_u.sort_values(by=self.nameO)

    # Name of columns
    df_u.columns = [self.nameO, self.codeO, self.nameF, self.codeF]

    # Return
    return df_u




  def update(self):
    """
    """

  def fit(self, values, acronym):
    """
    """

  def compute(self, input_path, output_path):
    """This method computes/updates a table from data.

    Parameters
    ----------
    input_path  : the path with the data.
    output_path : the path to store the table.

    Returns
    -------

    """
    # Create table using input data.
    tnew = self.create_table(input_path)
    told = pd_read.read_data(ftype='csv', path=output_path) 

    # Merge tables.
    dfm, dfc = tnew, None
    if told is not None:
      cols = [self.nameO, self.codeF]
      dfm, dfc = self.merge_table(told, tnew, self.nameO, self.codeF)
    
    # Sort and save.
    dfm.sort_values(by=self.nameO, inplace=True)
    dfm.to_csv(output_path, index=False)

    # Show information.
    self.show_information(dfm, dfc, output_path)

    # return
    return output_path



  def show_information(self, df, dfc, pathname):
    """This method shows important information.

    Parameters
    ----------

    Returns
    -------
    """
    # Text displayed as info when merging different files.
    txt_init = "Antibiotics table conversion created!\n"
    txt_merge = "\nThe following conflicts have been found. Please take action "
    txt_merge+= "by opening the automatically created antibiotic csv file "
    txt_merge+= "(antibotic database) and solving such conflicts before "
    txt_merge+= "continuing (by default the old values have been kept):"

    # Variables
    dup_nameO = df[df.duplicated(self.nameO)]
    dup_codeO = df[df.duplicated(self.codeO)]
    dup_codeF = df[df.duplicated(self.codeF)]

    # Print text init
    print("-"*80 + "\n"+txt_init)
    print("Different Original Names: %s" % len(df[self.nameO].unique()))
    print("Different Formated Names: %s " % len(df[self.nameF].unique()))
    print("Different Antibiotics Codes: %s\n" % len(df[self.codeF].unique()))

    # Print duplicates
    if len(dup_nameO)>0: print(dup_nameO)
    if len(dup_codeO)>0: print(dup_codeO)
    if len(dup_codeF)>0: print(dup_codeF)

    # Print conflicts
    if dfc is not None:
      print("Conflicts:")
      print(dfc)
      print(txt_merge)

    print("Please revise: %s" % pathname)
















class AntibioticTable():



  def __init__(self,  to_lowercase=None,
                      to_uppercase=None,
                      delete_spaces=None,
                      delete_parenthesis=None):
    """
    """
    self.to_lowercase = to_lowercase
    self.to_uppercase = to_uppercase
    self.delete_spaces = delete_spaces
    self.delete_parenthesis = delete_parenthesis


  def fit(self, dataframe):
    """
    """

    df_u = dataframe.replace(np.nan, "None")
    df_u = dataframe.groupby([self.nameO, self.codeO]).size()
    df_u = dataframe.reset_index().rename(columns={0:'count'})
    df_u = dataframe.replace("None", np.nan)

    print(df_u)
    """
    if self.to_lowercase is not None:

    if self.to_uppercase is not None:

    if self.delete_spaces is not None:

    if self.delete_parenthesis is not None:
    """





if __name__ == '__main__':

  # Import own module
  sys.path.append('../../../')

  # Import specific libraries
  from pyamr.datasets import load

  # Constants.
  goback = "../../../../"
  input_path = goback + "data/raw/microbiology/csv/luke02/"
  output_path = './antibiotics.csv'




  # ---------------------
  # load data
  # ---------------------
  # Load data
  data = load.dataset_epicimpoc_susceptibility_year(nrows=1000)

  # Tansform data
  data = data[['antibioticName', 'antibioticCode']]

  AntibioticTable().fit(data)

  # ---------------------
  # create builder
  # ---------------------
  # Builter
  builder = AntibioticsTable()
  print(data.columns)
  print(data.head(10))

  # Compute antibiotic table.
  builder.compute(input_path, output_path)
