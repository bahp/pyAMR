"""
SARI - Antibiogram
------------------

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


# -------------------------------------------
# Plot antibiogram clustered
# -------------------------------------------
#
# .. note:: See seaborn clustermap for configuration.
#
# .. warning:: nan converted to 1e-10 and used for distance.
#
#
# methods = ['single', 'complete', 'average', 'weighted',
#            'centroid', 'median', 'ward']
#
#
#

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


def _get_category_colors(series, cmap='tab20b', default='gray'):
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
  # Get unique elements
  unique = np.unique(series)
  # Sort unique values
  unique.sort()
  # Create the palette (gray for _na)
  palette = [default] + sns.husl_palette(len(unique), s=.45)
  # Create mappers from category to color
  mapper = dict(zip(map(str, unique), palette))
  # Create list with colors for each category.
  colors = pd.Series(series).map(mapper)
  # Return
  return colors

# Load datasets
abxs = pd.read_csv(path_abx)
orgs = pd.read_csv(path_org)

# Create mappers
abx_map = create_mapper(abxs, 'ANTIBIOTIC_CODE', 'ANTIBIOTIC_CLASS')
org_map = create_mapper(orgs, 'ORGANISM_CODE', 'GENUS_NAME')
grm_map = create_mapper(orgs, 'ORGANISM_CODE', 'GRAM_TYPE')

# Copy dataframe
dataframe = sari_overall.copy(deep=True)
dataframe = dataframe.reset_index()

# Include categories
dataframe['category'] = dataframe['ANTIBIOTIC'].map(abx_map)
dataframe['genus'] = dataframe['SPECIE'].map(org_map)
dataframe['gram'] = dataframe['SPECIE'].map(grm_map)

# Create matrix
matrix = sari_overall[['sari']]
matrix = matrix.unstack() * 100
matrix.columns = matrix.columns.droplevel()

# Create mask
mask = pd.isnull(matrix)

# Fill na
matrix = matrix.fillna(1e-10)

# Show
print(matrix.astype(int))

# Create colormap
cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

# Get categories
abx_class = matrix.columns \
    .to_series().replace(org_map).astype(str)
org_genus = matrix.index \
    .to_series().replace(org_map).astype(str)

# .. note: It is possible to also pass kwargs that would
#          be used by sns.heatmap function like annot, fmt,
#          annot_kws, ...

# Plot cluster map
grid = sns.clustermap(data=matrix, vmin=0, vmax=100,
    method='single', metric='euclidean', cmap=cmap,
    linewidth=0.05, mask=mask,
    row_colors=_get_category_colors(org_genus),
    col_colors=_get_category_colors(abx_class))

#

# Get tick labels.
yticklabels = pd.Series([e.get_text() \
    for e in grid.ax_heatmap.get_yticklabels()])
xticklabels = pd.Series([e.get_text() \
    for e in grid.ax_heatmap.get_xticklabels()])

# Create new
g = yticklabels.replace(org_map).astype(str)
c = xticklabels.replace(abx_map).astype(str)

yticklabels = ['{0} ({1})'.format(org, genus) \
    for genus, org in zip(g, yticklabels)]
#xticklabels = ['{0} ({1})'.format(abx, clss) \
#    for clss, abx in zip(c, yticklabels)]


grid.ax_heatmap.set_yticklabels(yticklabels)
#grid.ax_heatmap.set_yticklabels(xticklabels)

#
plt.suptitle('Antibiogram (clustered)')
plt.tight_layout()

plt.show()