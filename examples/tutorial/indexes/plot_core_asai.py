"""
Index - ASAI
============================

Example using your package
"""


# Import libraries
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
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


# ---------------------
# helper method
# ---------------------
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


# ---------------------
# Create data
# ---------------------
# Create data
data = [['GENUS_1', 'SPECIE_1', 'ANTIBIOTIC_1', 'N', 0.6000, 0.05],
        ['GENUS_2', 'SPECIE_2', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
        ['GENUS_2', 'SPECIE_3', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
        ['GENUS_2', 'SPECIE_4', 'ANTIBIOTIC_1', 'N', 0.0064, 0.05],
        ['GENUS_2', 'SPECIE_5', 'ANTIBIOTIC_1', 'N', 0.0073, 0.05],
        ['GENUS_2', 'SPECIE_6', 'ANTIBIOTIC_1', 'N', 0.0056, 0.05],
        ['GENUS_3', 'SPECIE_7', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
        ['GENUS_4', 'SPECIE_8', 'ANTIBIOTIC_1', 'N', 0.0518, 0.05],
        ['GENUS_4', 'SPECIE_9', 'ANTIBIOTIC_1', 'N', 0.0000, 0.05],
        ['GENUS_4', 'SPECIE_10', 'ANTIBIOTIC_1', 'N', 0.0595, 0.05],

        ['GENUS_1', 'SPECIE_1', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_2', 'SPECIE_2', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_2', 'SPECIE_3', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_2', 'SPECIE_4', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_2', 'SPECIE_5', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_2', 'SPECIE_6', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_3', 'SPECIE_7', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_4', 'SPECIE_8', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_4', 'SPECIE_9', 'ANTIBIOTIC_1', 'P', 0.0, 0.05],
        ['GENUS_5', 'SPECIE_10', 'ANTIBIOTIC_1', 'P', 0.0, 0.05]]

# Create dataframe
dataframe = pd.DataFrame(data, columns=['GENUS',
                                        'SPECIE',
                                        'ANTIBIOTIC',
                                        'GRAM',
                                        'RESISTANCE',
                                        'THRESHOLD'])

# -------------------------------
# Create antimicrobial spectrum
# -------------------------------
# Create antimicrobial spectrum of activity instance
asai = ASAI(weights='uniform', threshold=0.05,
            column_genus='GENUS',
            column_specie='SPECIE',
            column_antibiotic='ANTIBIOTIC',
            column_resistance='RESISTANCE',
            column_threshold='THRESHOLD')

# Compute
scores = asai.compute(dataframe, by_category='GRAM')

# Show
print(scores)

# -----------------------------
# Plot
# -----------------------------
# Variables to plot.
x = scores.index.values
y_n = scores['ASAI_SCORE']['N'].values
y_p = scores['ASAI_SCORE']['P'].values

# Constants
colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

# Create figure
f, ax = plt.subplots(1, 1, figsize=(8, 0.5))

# Plot
sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h',
            saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h',
            saturation=0.5, label='Gram-negative')

# Configure
sns.despine(bottom=True)

# Configure
ax.set_xlim([-1, 1])

# Legend
plt.legend()

# Display
plt.show()