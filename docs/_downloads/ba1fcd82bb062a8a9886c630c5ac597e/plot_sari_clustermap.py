"""
SARI - Antibiogram (clustered)
------------------------------

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
from pyamr.core.freq import Frequency
from pyamr.core.sari import SARI
from pyamr.datasets.load import load_data_mimic

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


# --------------------------------------------------------------------
#                               Main
# --------------------------------------------------------------------
# Load data
data, antibiotics, organisms = load_data_mimic()

# Count records per specimen code
specimen_code_count = data \
    .groupby('laboratory_number').head(1) \
    .specimen_code.value_counts(normalize=True) \
    .sort_values(ascending=False)

# Filter most frequent specimens
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:5])]

# Create sari instance
sari = SARI(groupby=['specimen_code',
                     'microorganism_name',
                     'antimicrobial_name',
                     'sensitivity'])

# Compute SARI overall
sari_overall = sari.compute(data,
    return_frequencies=True)

# Show
print("SARI (overall):")
print(sari_overall)


# ------------------------------
# Include registries information
# ------------------------------
# Libraries
from pyamr.datasets.registries import MicroorganismRegistry
from pyamr.datasets.registries import AntimicrobialRegistry

# Load registry
mreg = MicroorganismRegistry()
areg = AntimicrobialRegistry()

# Format sari dataframe
dataframe = sari_overall.copy(deep=True)
dataframe = dataframe.reset_index()

# Create genus and species
dataframe[['genus', 'species']] = \
    dataframe.microorganism_name \
        .str.capitalize() \
        .str.split(expand=True, n=1)

# Combine with registry information
dataframe = mreg.combine(dataframe)
dataframe = areg.combine(dataframe)


# -------------------------------------------
# Plot
# -------------------------------------------
# Libraries
from pyamr.utils.plot import get_category_colors

# Reset
sari_overall = dataframe.reset_index()

# Loop
for specimen, df in sari_overall.groupby(by='specimen_code'):

    # -------------------------------
    # Create matrix
    # -------------------------------
    # Filter
    matrix = df.copy(deep=True)
    matrix = df.reset_index()

    # Pivot table
    matrix = pd.pivot_table(matrix,
         index=['microorganism_name', 'genus'],
         columns=['antimicrobial_name', 'category'],
         values='sari')

    # Convert to percent
    matrix = matrix * 100

    # Create mask
    mask = pd.isnull(matrix)

    # Fill missing (error when computing distance)
    matrix = matrix.fillna(1e-10)

    # Show
    print("\n\n\nData (%s)" % specimen)
    print(matrix.astype(int))

    # -------------------------------
    # Plot
    # -------------------------------
    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Row and col colors
    col_colors = get_category_colors( \
        index=matrix.columns, category=matrix.columns.names[1])
    row_colors = get_category_colors( \
        index=matrix.index, category=matrix.index.names[1])

    # .. note: It is possible to also pass kwargs that would
    #          be used by sns.heatmap function (annot, fmt,
    #          annot_kws, ...
    try:
        # Plot cluster map
        grid = sns.clustermap(data=matrix, vmin=0, vmax=100,
            method='centroid', metric='euclidean', cmap=cmap,
            linewidth=0.05, mask=mask, square=True,
            row_colors=row_colors, col_colors=col_colors)
    except Exception as e:
        print("Exception: %s" % e)

    # Configuration
    plt.suptitle('Antibiogram (clustered) - %s' % specimen, fontsize=12)
    plt.tight_layout()

# Show
plt.show()