"""
ASAI - multiple
---------------

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
y_u = scores['ASAI_SCORE']['u'].values

# Constants
colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)
colormap_u = scalar_colormap(y_u, cmap='Greens', vmin=-0.1, vmax=1.1)

# ----------
# Example
# ----------
# This example shows an stacked figure using more than two categories. 
# For instance, it uses gram-positive, gram-negative and gram-unknown. 
# All theindexes go within the range [0,1].
# Create the figure
f, axes = plt.subplots(1, 3, figsize=(7, 4))

# Plot each category
sns.barplot(x=y_p, y=x, palette=colormap_p, ax=axes[0], orient='h', 
  saturation=0.5, label='Gram-positive')
sns.barplot(x=y_n, y=x, palette=colormap_n, ax=axes[1], orient='h', 
  saturation=0.5, label='Gram-negative')
sns.barplot(x=y_u, y=x, palette=colormap_u, ax=axes[2], orient='h', 
  saturation=0.5, label='Gram-unknown')

# Configure
sns.despine(bottom=True)

# Format figure
plt.subplots_adjust(wspace=0.0, hspace=0.0)

# Remove yticks
axes[1].set_yticks([])
axes[2].set_yticks([])

# Set title
axes[0].set_title('Gram-positive')
axes[1].set_title('Gram-negative')
axes[2].set_title('Gram-unknown')

# Set x-axis
axes[0].set_xlim([0,1.1])
axes[1].set_xlim([0,1.1])
axes[2].set_xlim([0,1.1])

# Adjust
plt.tight_layout()

# Show
plt.show()
