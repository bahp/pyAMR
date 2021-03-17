"""
Visualization - antibiogram
----------------------------

The example below loads a portion of the culture dataset and creates the 
pipeline to remove outliers, imput missing data, address the class imbalance 
and scale the data features accordingly. After this, a number of estimators 
are trained and tested (see wrappers and grids). The results such as the
estimators (pickle) and metrics (csv) re stored in the specified path.

@see core
@see xxx
"""

# Import libraries
import sys
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.datasets import load
from pyamr.core.freq import Frequency
from pyamr.core.sari import SARI
from pyamr.core.asai import ASAI
from pyamr.core.table.acronym import AcronymBuilder
from pyamr.graphics.antibiogram import Antibiogram

# Ignore warnings
warnings.simplefilter('ignore')

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


# -------------------------
# load susceptibility data
# -------------------------
# Load data
data = load.dataset_epicimpoc_susceptibility(nrows=10000)

# Filter required columns
data = data[['antibioticCode',
             'organismCode',
             'dateReceived',
             'sensitivity',
             'orderCode']]

# Select specific examples
#is_cod = data['orderCode']=='URICUL'
#is_org = data['organismCode']=='ECOL'
#is_abx = data['antibioticCode'].isin(['ATAZ', 'AMER'])
#data = data[is_cod & is_abx & is_org]

# Show
print("\n\nData input:")
print(data.head(10))

# --------------------
# compute frequencies
# --------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
                 column_organism='organismCode',
                 column_date='dateReceived',
                 column_outcome='sensitivity')

# Compute frequencies overall
freq_overall = freq.compute(data, strategy='overall', 
                                  by_category='pairs')

# ------------------------
# compute resistance index
# ------------------------
# Compute sari
sari_overall = SARI(strategy='medium').compute(freq_overall)

# ------------------------
# format dataframe
# ------------------------

def create_mapper(dataframe, column_key, column_value):
  """This method constructs a mapper

  Parameters
  ----------
  dataframe: dataframe-like
    The dataframe from which the columns are extracted

  column_key: string-like
    The name of the column with the values for the keys of the mapper

  column_value: string-like
    The name of the column with the values for the values of the mapper

  Returns
  -------
  dictionary
  """
  dataframe = dataframe[[column_key, column_value]]
  dataframe = dataframe.drop_duplicates()
  return dict(zip(dataframe[column_key], dataframe[column_value]))

# Load datasets
antibiotics = load.dataset_epicimpoc_antibiotics()
organisms = load.dataset_epicimpoc_organisms()

# Create mappers
abx_map = create_mapper(antibiotics, 'antibioticCode', 'antibioticClass')
org_map = create_mapper(organisms, 'organismCode', 'specieName')

# Copy dataframe
dataframe = sari_overall.copy(deep=True)
dataframe = dataframe.reset_index()

# Include categories
dataframe['category'] = dataframe['ANTIBIOTIC'].map(abx_map)
dataframe['genus'] = dataframe['SPECIE'].map(org_map)

# Show dataframe
print("\n\nData antibiogram:")
print(dataframe.head(10))

# ------------------------
# create antibiogram
# ------------------------
# Antibiogram plotter
antibiogram = Antibiogram(column_organism='SPECIE',
                          column_antibiotic='ANTIBIOTIC',
                          column_genus='genus',
                          column_category='category',
                          column_index='sari')

# Fit antibiogram
antibiogram = antibiogram.fit(dataframe)

# ---------
# Example 1
# ----------
antibiogram.plot(genera=['staphylococcus',
                          'klebsiella',
                          'streptococcus',
                          'enterococcus'],
                 method='weighted',
                 metric='euclidean',
                 figsize=(15,8))

# Show
plt.show()
