"""
ASAI - gram type
----------------

.. todo:: Explain...

"""

# Import libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.datasets import load
from pyamr.core.asai import ASAI

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
# Save
dataframe = pd.read_csv('../_data/data-spectrum.csv')

# Empty grams are a new category (unknown - u)
dataframe.loc[pd.isnull(dataframe['gram']), 'gram'] = 'u'

# Show
print("Data input:")
print(dataframe.head(10))

# -------------------------------
# Create antimicrobial spectrum
# -------------------------------
# Create antimicrobial spectrum of activity instance
asai = ASAI(weights='uniform', threshold=0.05,
                               column_genus='specie',
                               column_specie='genus', 
                               column_antibiotic='antibiotic', 
                               column_resistance='resistance')

# Compute
scores = asai.compute(dataframe, by_category='gram')

# -------------------------------
# Filter and reoorder
# -------------------------------
# Antibiotics to display
abxs_urine = ['cephalexin', 'ciprofloxacin', 'ampicillin', 'trimethoprim',
  'augmentin', 'meropenem', 'nitrofurantoin', 'amikacin', 'cefotaxime',
  'tazocin', 'gentamicin', 'ertapenem', 'ceftazidime', 'mecillinam',
  'cefoxitin', 'vancomycin', 'clindamycin', 'erythromycin', 'aztreonam',
  'tigecycline', 'amoxycillin']

# Filter by antibiotics
scores = scores[scores.index.isin(abxs_urine)]

# Sort
scores = scores.fillna(0.0)
scores['width'] = np.abs(scores['ASAI_SCORE']['n']+scores['ASAI_SCORE']['p'])
scores['gmean'] = np.sqrt(scores['ASAI_SCORE']['n']*scores['ASAI_SCORE']['p'])
scores = scores.sort_values(by='gmean', ascending=False)

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
f, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)

# Plot with pallete according to value
sns.barplot(x=y_p, y=x, ax=axes[0], orient='h', palette=colormap_p,
  saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, ax=axes[0], orient='h', palette=colormap_n,
  saturation=0.5, label='Gram-negative')

# Plot with plain pallete (values are already size of bars)
sns.barplot(x=y_p, y=x, ax=axes[1], orient='h', color='b',
  saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, ax=axes[1], orient='h', color='r',
  saturation=0.5, label='Gram-negative')

# Configure
sns.despine(bottom=True)

# Show legend.
plt.legend()

# Adjust
plt.tight_layout()

# Show
plt.show()
