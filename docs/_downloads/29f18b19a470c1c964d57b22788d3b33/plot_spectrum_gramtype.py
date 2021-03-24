"""
ASAI - gram type
----------------

.. warning:: Implement using sample data.

"""

# Import libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.core.asai import ASAI
from pyamr.core.sari import SARI
from pyamr.core.freq import Frequency
from pyamr.datasets.load import make_susceptibility

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

# ------------------------
# Methods
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


# -------------------------------------------
# Load data
# -------------------------------------------
# Load data
data = make_susceptibility()

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)


# -------------------------------------------
# Compute Freq and SARI
# -------------------------------------------
# Create instance
freq = Frequency(column_antibiotic='antimicrobial_code',
                 column_organism='microorganism_code',
                 column_date='date_received',
                 column_outcome='sensitivity')

# Compute frequencies (overall)
freq_overall = freq.compute(data, by_category='pairs')

# Compute SARI
sari_overall = SARI(strategy='hard').compute(freq_overall)


# -------------------------------------------
# Compute Freq and SARI
# -------------------------------------------
# Create mappers
genus_map = create_mapper(data, 'microorganism_code', 'microorganism_genus')
gramt_map = create_mapper(data, 'microorganism_code', 'microorganism_gram_type')

# Create matrix
matrix = sari_overall.copy(deep=True)
matrix = matrix.reset_index()
matrix['microorganism_genus'] = matrix.SPECIE.map(genus_map)
matrix['microorganism_gram_type'] = matrix.SPECIE.map(gramt_map)

# Create instance
asai = ASAI(weights='uniform',
            threshold=0.05,
            column_genus='microorganism_genus',
            column_specie='SPECIE',
            column_antibiotic='ANTIBIOTIC',
            column_resistance='sari')
# Compute
scores = asai.compute(matrix,
    by_category='microorganism_gram_type')


# -------------------------------
# Filter and reoorder
# -------------------------------
# Sort
scores = scores.fillna(0.0)
scores['width'] = np.abs(scores['ASAI_SCORE']['n']+scores['ASAI_SCORE']['p'])
scores['gmean'] = np.sqrt(scores['ASAI_SCORE']['n']*scores['ASAI_SCORE']['p'])
scores = scores.sort_values(by='width', ascending=False)

# Show scores
print("Data output:")
print(scores)


# ----------------
# Plot
# ----------------
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
# and gram-negative categories. Note that the gram negative categorie has
# values in the range [-1,0] while the gram-positive category has values
# within the range [0, 1]
# Create figure
f, axes = plt.subplots(1, 2, figsize=(7, 8), sharey=True)

# Plot with pallete according to value
sns.barplot(x=y_p, y=x, ax=axes[0], orient='h', palette=colormap_p,
  saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, ax=axes[0], orient='h', palette=colormap_n,
  saturation=0.5, label='Gram-negative')

# Plot with plain palette (values are already size of bars)
sns.barplot(x=y_p, y=x, ax=axes[1], orient='h', color='b',
  saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, ax=axes[1], orient='h', color='r',
  saturation=0.5, label='Gram-negative')

# Configure
sns.despine(bottom=True)

# Configure axes
axes[0].set(title='ASAI (width)')
axes[1].set(title='ASAI (width)')

# Show legend.
plt.legend()

# Adjust
plt.tight_layout()

# Show
plt.show()
