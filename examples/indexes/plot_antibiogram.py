"""
SARI - Antibiogram
------------------

.. todo:: Explain...

"""
"""
# Libraries
import sys
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
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
dataframe = pd.read_csv('../_data/data-antibiogram.csv')

# Show data
print("Data input:")
print(dataframe.head(10))

print(dataframe.columns)

# -------------------------------------------
# Load data
# -------------------------------------------
# Path
path = '../../pyamr/datasets/other/susceptibility.csv'
path_org = '../../pyamr/datasets/other/organisms.csv'
path_abx = '../../pyamr/datasets/other/antibiotics.csv'

# Columns
usecols = ['dateReceived',
           'labNumber',
           'patNumber',
           'orderName',
           'orderCode',
           'organismName',
           'organismCode',
           'antibioticName',
           'antibioticCode',
           'sensitivity']

# Load data
data = pd.read_csv(path, usecols=usecols,
    parse_dates=['dateReceived'])

# Clean
data = data.drop_duplicates()

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)

# -------------------------------------------
# Compute Freq
# -------------------------------------------
# Import specific libraries
from pyamr.core.freq import Frequency

# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
              column_organism='organismCode',
              column_date='dateReceived',
              column_outcome='sensitivity')

# Compute frequencies (overall)
freq_overall = freq.compute(data, by_category='pairs')

# -------------------------------------------
# Compute SARI
# -------------------------------------------
# Import specific libraries
from pyamr.core.sari import SARI

# Compute SARI
sari_overall = SARI(strategy='hard').compute(freq_overall)




# -------------------------------
# Create antibiogram
# -------------------------------
# Load default organisms dataset
orgs = pd.read_csv(path_org,
 usecols=['ORGANISM_NAME',
          'ORGANISM_CODE',
          'GENUS_NAME',
          'GENUS_CODE',
          'GRAM_TYPE'])

# Load default organisms dataset
abxs = pd.read_csv(path_abx,
 usecols=['ANTIBIOTIC_NAME',
          'ANTIBIOTIC_CODE',
          'ANTIBIOTIC_CLASS'])


# Format DataFrame
dataframe = sari_overall.reset_index()
dataframe = dataframe.merge(orgs, how='left',
    left_on='SPECIE', right_on='ORGANISM_CODE')
dataframe = dataframe.merge(abxs, how='left',
    left_on='ANTIBIOTIC', right_on='ANTIBIOTIC_CODE')


print(dataframe)

# Antibiogram plotter
antibiogram = Antibiogram(column_organism='SPECIE',
                          column_antibiotic='ANTIBIOTIC',
                          column_genus='GENUS_NAME',
                          column_category='ANTIBIOTIC_CLASS',
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
"""