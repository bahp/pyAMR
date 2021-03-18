"""
SART - by gram type
-------------------

.. todo: Simplify and explain
"""

# Import libraries
import sys
import glob
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
# load suspcetibility data
# -------------------------
path_sus = '../../resources/data/nhs/susceptibility/complete/'
path_abx = '../../resources/data/nhs/antibiotics/antibiotics.csv'
path_org = '../../resources/data/nhs/organisms/organisms.csv'

# Interesting columns
usecols = ['dateReceived',
           'organismCode',
           'antibioticCode',
           'sensitivity']

# Load all files
data = pd.concat([  \
    pd.read_csv(f, parse_dates=['dateReceived'],
        usecols=usecols) for f in glob.glob(path_sus + "/*.csv")])

# Filter for two examples
#is_org = data['organismCode']=='ECOL'
#is_abx = data['antibioticCode'].isin(['ATAZ', 'AMER'])
#data = data[is_abx & is_org]


# Show
print("\nData:")
print(data)


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
antibiotics = pd.read_csv(path_abx)
organisms = pd.read_csv(path_org)

# Create mappers
abx_map = create_mapper(antibiotics, 'antibioticCode', 'antibioticClass')
org_map = create_mapper(organisms, 'organismCode', 'specieName')
grm_map = create_mapper(organisms, 'organismCode', 'gramType')

# Copy dataframe
dataframe = sari_overall.copy(deep=True)
dataframe = dataframe.reset_index()

# Include categories
dataframe['category'] = dataframe['ANTIBIOTIC'].map(abx_map)
dataframe['genus'] = dataframe['SPECIE'].map(org_map)
dataframe['gram'] = dataframe['SPECIE'].map(grm_map)

# ------------------------
# compute spectrum index
# ------------------------
# Create antimicrobial spectrum of activity instance
asai = ASAI(weights='uniform', threshold=0.05,
                               column_genus='genus',
                               column_specie='SPECIE',
                               column_antibiotic='ANTIBIOTIC',
                               column_resistance='sari')

# Compute
scores = asai.compute(dataframe, by_category='gram')

# Show scores
print("\n\nData ASAI:")
print(scores.head(10))

# ---------------------------------------
# plot
# ---------------------------------------
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


# Sort
scores = scores.fillna(0.0)
scores['width'] = np.abs(scores['ASAI_SCORE']['n']+scores['ASAI_SCORE']['p'])
scores['gmean'] = np.sqrt(scores['ASAI_SCORE']['n']*scores['ASAI_SCORE']['p'])
scores = scores.sort_values(by='gmean', ascending=False)

# Variables to plot.
x = scores.index.values
y_n = scores['ASAI_SCORE']['n'].values
y_p = scores['ASAI_SCORE']['p'].values

# Constants
colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

# ----------
# Example
# ----------
# This example shows a diverging figure using exclusively the gram-positive
# and gram-negative categories. Note that the gram negative categories has
# values in the range [-1,0] while the gram-positive category has values
# within the range [0, 1]
# Create figure
f, ax = plt.subplots(1, 1, figsize=(3, 9))

# Plot
sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h',
 saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h',
 saturation=0.5, label='Gram-negative')

# Configure
sns.despine(bottom=True)

# Show legend.
plt.legend(loc=8)
plt.subplots_adjust(left=0.4, right=0.9, bottom=0.05, top=0.98)

# Show
plt.show()