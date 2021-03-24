"""
SARI - Clustermap (overall)
---------------------------

.. todo:: Explain...

"""

# Libraries
import sys
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
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
# Plot antibiogram clustered
# -------------------------------------------

# -------------------------------
# Create matrix
# -------------------------------
# Create mappers
abx_map = create_mapper(data, 'antimicrobial_code', 'antimicrobial_class')
org_map = create_mapper(data, 'microorganism_code', 'microorganism_genus')

# Create matrix
matrix = sari_overall.reset_index()
matrix['microorganism_genus'] = matrix.SPECIE.map(org_map)
matrix['antimicrobial_class'] = matrix.ANTIBIOTIC.map(abx_map)

# Pivot table
matrix = pd.pivot_table(matrix, values='sari',
   index=['SPECIE', 'microorganism_genus'],
   columns=['ANTIBIOTIC', 'antimicrobial_class'])

# Convert to percent
matrix = matrix * 100

# Create mask
mask = pd.isnull(matrix)

# Fill missing (error when computing distance)
matrix = matrix.fillna(1e-10)

# Show
print("\nData")
print(matrix.astype(int))

# ------------------
# Plot
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

# Plot cluster map
grid = sns.clustermap(data=matrix, vmin=0, vmax=100,
    method='centroid', metric='euclidean', cmap=cmap,
    linewidth=0.05, mask=mask,
    row_colors=row_colors, col_colors=col_colors)

# Configuration
plt.suptitle('Antibiogram (clustered)', fontsize=12)
plt.tight_layout()

# Show
plt.show()