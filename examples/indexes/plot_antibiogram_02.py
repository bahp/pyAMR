"""
SARI - Antibiogram (by culture)
-------------------------------

.. todo:: Explain...

"""

# Libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
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

# ------------------
# Methods
# ------------------
def get_category_colors(index, category, cmap='tab10'):
    """This method creates the colors for the different elements in
    categorical feature vector.

    Parameters
    ----------
    values : array-like
        The vector with the categorical values

    cmap: string-like
        The colormap to use

    default: string-like
        The color to be used for the first value. Note that this
        value needs to appear first on the the sorted list, as such
        it is recommended to set is as _default.

    Returns
    -------
    """
    # Get categories
    categories = index.get_level_values(category)
    # Get unique elements
    unique = np.unique(categories)
    # Create the palette
    palette = sns.color_palette(cmap, desat=0.5, n_colors=unique.shape[0])
    # Create mappers from category to color
    mapper = dict(zip(map(str, unique), palette))
    # Create list with colors for each category
    colors = pd.Series(categories, index=index).map(mapper)
    # Return
    return colors


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
# For each culture type
# -------------------------------------------
# Count records per order code
specimen_code_count = data.specimen_code.value_counts()

# Filter most frequent order codes
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:5])]

# Loop
for specimen_code, df in data.groupby(by='specimen_code'):

    # -------------------------------------------
    # Compute Freq and SARI
    # -------------------------------------------
    # Create instance
    freq = Frequency(column_antibiotic='antimicrobial_code',
                     column_organism='microorganism_code',
                     column_date='date_received',
                     column_outcome='sensitivity')

    # Compute frequencies (overall)
    freq_overall = freq.compute(df, by_category='pairs')

    # Compute SARI
    sari_overall = SARI(strategy='hard').compute(freq_overall)

    # ------------
    # Plot Heatmap
    # ------------
    # Create matrix
    matrix = sari_overall[['sari']]
    matrix = matrix.unstack() * 100
    matrix.columns = matrix.columns.droplevel()

    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(8,8))

    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Specify cbar axes
    #cbar_ax = f.add_axes([.925, .3, .05, .3])

    # Plot
    ax = sns.heatmap(data=matrix, annot=True, fmt=".0f",
                     annot_kws={'fontsize': 7}, cmap=cmap,
                     linewidth=0.5, vmin=0, vmax=100, ax=ax,
                     xticklabels=1, yticklabels=1)
                     # cbar_ax=cbar_ax)

    # Configure axes
    ax.set(aspect="equal")

    # Set rotation
    plt.yticks(rotation=0)

    # Add title
    plt.suptitle("Antibiogram (%s)" % specimen_code,
        fontsize=15)

    # Tight layout
    plt.tight_layout()
    #plt.subplots_adjust(right=0.91)

# Show
plt.show()