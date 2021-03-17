"""
SARI - Antibiogram
------------------

.. todo:: Explain and Simplify

.. todo: Frequency might not be working?
         Frequency can be computed as sum of columns.

"""

# Libraries
import sys
import glob
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
from pyamr.datasets import load
from pyamr.core.freq import Frequency
from pyamr.core.sari import SARI
from pyamr.graphics.antibiogram import Antibiogram

# -------------------------
# Configuration
# -------------------------
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


# -------------------------------
# Load data
# -------------------------------
# Load
#dataframe = pd.read_csv('../_data/data-antibiogram.csv')
# Path to susceptibility data
path_sus = '../../resources/data/nhs/susceptibility/complete/'
path_abx = '../../resources/data/nhs/antibiotics/antibiotics.csv'
path_org = '../../resources/data/nhs/organisms/organisms.csv'

# Interesting columns
usecols = ['dateReceived',
           'orderCode',
           'orderName',
           'specimenType',
           'labNumber',
           'patNumber',
           'organismName',
           'organismCode',
           'antibioticName',
           'antibioticCode',
           'sensitivity']

# Load all files
dataframe = pd.concat([  \
    pd.read_csv(f, parse_dates=['dateReceived'],
        usecols=usecols) for f in glob.glob(path_sus + "/*.csv")])

# Show
print("\nData:")
print(dataframe)


# --------------------
# compute frequencies
# --------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
                 column_organism='organismCode',
                 column_date='dateReceived',
                 column_outcome='sensitivity')

# Compute frequencies overall
freq_overall = freq.compute(dataframe, strategy='overall',
                                       by_category='pairs')

# Show
print("\nFrequencies:")
print(freq_overall.head(10))

# ------------------------
# compute resistance index
# ------------------------
# Compute sari
sari_overall = SARI(strategy='medium').compute(freq_overall)

# Show
print("\nSARI:")
print(sari_overall.head(10))


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
antibiotics = pd.read_csv(path_abx)
organisms = pd.read_csv(path_org)

# Create mappers
abx_map = create_mapper(antibiotics, 'antibioticCode', 'antibioticClass')
org_map = create_mapper(organisms, 'organismCode', 'specieName')

# Copy dataframe
dataframe = sari_overall.copy(deep=True)
dataframe = dataframe.reset_index()


# Include categories
dataframe['category'] = dataframe['ANTIBIOTIC'].map(abx_map)
dataframe['genus'] = dataframe['SPECIE'].map(org_map)

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

print("Total records")
print(dataframe[['intermediate', 'resistant', 'sensitive']].sum().sum())

# Show
plt.show()