################################################################################
# Author:
# Date:
# Description:
#
#
#
# Copyright:
#
# 
################################################################################
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

# -------------------------------------------------------------------------
#                            helper methods
# -------------------------------------------------------------------------
def _get_colors(index, column, palette):
  """This method gets the colors for each index value.

  Parameters
  ----------
  index :

  column :

  palette:

  Returns
  -------
  """
  # Get species
  species = index.get_level_values(column).unique().sort_values()
  netwpal = ['gray'] + sns.husl_palette(len(species), s=.45)
  #netwpal = ['gray'] + list(sns.color_palette('Set2', len(species)+1, .75))
  #netwpal = ['gray'] + list(sns.color_palette(palette, len(species)+1, .45))
  netwmap = dict(zip(map(str, species), netwpal))
  # Convert the palette to vectors that will be drawn on the side of the matrix
  networks = index.get_level_values(column)
  network_colors = pd.Series(networks, index=index).map(netwmap)
  # Return
  return species, netwpal, network_colors

# -------------------------------------------------------------------------
#                                main
# -------------------------------------------------------------------------
# -------------------------------
# Load data
# -------------------------------
# The loaded data needs to have the following columns: 



# Load dataframe
dataframe = pd.read_csv('./antibiogram-sample.csv')

# Format dataframe
dataframe = dataframe.set_index(['organismCode', 
                                 'antibioticCode', 
                                 'specieName',
                                 'antibioticClass'])

# Create heatmap
dataframe = dataframe.unstack(['antibioticCode', 
                               'antibioticClass'])

# Remove intrinsic resistnace
dataframe[dataframe==1] = np.nan
dataframe = dataframe.fillna(1e-10)

# --------------------------------
# Configure plot
# --------------------------------
# Parameters
method = 'weighted'
metric = 'euclidean'

# Create mask
mask = pd.isnull(dataframe)

# Create colormap
colormap = sns.color_palette("Reds", desat=0.5, n_colors=10)

vals1, pal1, col1 = _get_colors(dataframe.index, 'specieName', 'nipy_spectral')
vals2, pal2, col2 = _get_colors(dataframe.columns, 'antibioticClass', 'tab20b')

# --------------------------------
# Plot
# --------------------------------


# Plot
grid = sns.clustermap(dataframe, center=0.5, method=method, metric=metric, 
    vmin=0.0, vmax=1.0, mask=mask, cmap=colormap, linewidths=.75, 
    figsize=(5,5), xticklabels=True, yticklabels=True,
    row_colors=col1, col_colors=col2)

plt.subplots_adjust(bottom=0.3, top=0.9, left=0.05, right=0.7)
plt.title('%s, %s' % (method, metric))

labelsx = ['(%s) %5s' % (e.get_text().split('-')[2],
                     e.get_text().split('-')[1])
            for e in grid.ax_heatmap.get_xticklabels()]
labelsy = ['%-6s (%s)' % (e.get_text().split('-')[0],
                     e.get_text().split('-')[1])
             for e in grid.ax_heatmap.get_yticklabels()]

grid.ax_heatmap.set_xticklabels(labelsx)
grid.ax_heatmap.set_yticklabels(labelsy)

plt.show()
