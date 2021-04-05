"""
SARI - Clustermap (by specimen)
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
def get_category_colors(index, category, cmap='hls'):
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
# Compute SARI
# -------------------------------------------
# Libraries
from pyamr.core.sari import SARI

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

print(dataframe.dtypes)

# -------------------------------------------
# Plot
# -------------------------------------------
# Reset
sari_overall = dataframe.reset_index()

# Count records per specimen
specimen_count = dataframe \
    .groupby('specimen_code').freq.sum() \
    .sort_values(ascending=False)

# Show
print("Cultures:")
print(specimen_count)

# Filter
dataframe = dataframe[dataframe \
    .specimen_code.isin( \
        specimen_count.index.values[:5])]

# Loop
for specimen, df in dataframe.groupby(by='specimen_code'):

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