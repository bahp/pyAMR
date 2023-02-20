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
from __future__ import division

# Libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt



# -----------------------------------------------------------------------------
#                               helper methods
# -----------------------------------------------------------------------------
def _get_category_colors(values, cmap='tab20b', default='gray'):
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
  unique = np.unique(values)
  # Sort unique values
  unique.sort()
  # Create the palette (gray for _na)
  palette = [default] + sns.husl_palette(len(unique), s=.45)
  # Create mappers from category to color
  mapper = dict(zip(map(str, unique), palette))
  # Create list with colors for each category.
  colors = pd.Series(values).map(mapper)
  # Return
  return colors


def _idxs(index, level, values):
  """
  """
  return index.get_level_values(level).isin(values)

def _get_colors(index, column, palette):
  """This method gets the colors for each index value.

  # Get species
  vals1, pal1, row_colors = \
    _get_colors(dataframe.index, self.c_gen, 'nipy_spectral')
  vals2, pal2, col_colors = \
    _get_colors(dataframe.columns, self.c_cat, 'tab20b')


  Parameters
  ----------
  index:

  column:

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




class Antibiogram:
    """"""

    # Attributes
    c_cat = 'CATEGORY'
    c_abx = 'ANTIBIOTIC'
    c_org = 'SPECIE'
    c_gen = 'GENUS'
    c_idx = 'SARI'

    def __init__(self, column_organism=c_org,
                     column_antibiotic=c_abx,
                     column_genus=c_gen,
                     column_category=c_cat,
                     column_index=c_idx,
                     colormap_genus='nipy_spectral',
                     colormap_category='tab20b',
                     discard_intrinsic=False):
        """The constructor.

        Parameters
        ----------
        column_organism: string-like
          The column name with the the organism values

        column_antibiotic: string-like
          The column name with the the antibiotic values

        column_genus: string-lik
          The column name with the the organism genus values

        columns_category: string-like
          The column name with the the antibiotic category values

        colormap_genus: string-like
          The colormap to use to display the genus values

        colormap_category: string-like
          The colormap to use to display the category values

        discard_intrinsic: string-like
          Wether or not to remove the intrinsic resistance indexes. These are
          defined as those indexes in which the microbiology was neven found
          to be sensitivity and therefore has a resistance index of 1.

        Returns
        -------
        """
        # Set parameters
        self.colormap_genus = colormap_genus
        self.colormap_category = colormap_category
        self.discard_intrinsic = discard_intrinsic

        # Create dictionary to rename columns
        self.rename_columns = {column_antibiotic: self.c_abx,
                               column_organism: self.c_org,
                               column_genus: self.c_gen,
                               column_category: self.c_cat,
                               column_index: self.c_idx}



    def fit(self, dataframe):
        """This method fits the antibiogram to the data.

        Parameters
        ----------
        dataframe: pd.DataFrame
            The...

        Returns
        -------
        Antibiogram instance
        """
        # Check that it is a dataframe
        if not isinstance(dataframe, pd.DataFrame):
          raise TypeError("The instance passed as argument needs to be a pandas "
                          "DataFrame. Instead, a <%s> was found. Please convert "
                          "the input accordingly." % type(dataframe))

        # Rename columns
        self._dataframe = \
          dataframe.rename(columns=self.rename_columns, copy=True)

        # Fill missing categories (so they have same color)
        self._dataframe[self.c_org].fillna('_na', inplace=True)
        self._dataframe[self.c_cat].fillna('_na', inplace=True)

        # Keep only interesting rows
        self._dataframe = self._dataframe[self.rename_columns.values()]

        # Format dataframe
        self._dataframe = self._dataframe.set_index([self.c_org,
                                                     self.c_abx,
                                                     self.c_gen,
                                                     self.c_cat])

        # Create heatmap
        self._dataframe = self._dataframe.unstack([self.c_abx,
                                                   self.c_cat])

        # Drop sari index
        self._dataframe.columns = self._dataframe.columns.droplevel()

        # Discard intrinsic resistance
        if not self.discard_intrinsic:
          self._dataframe[self._dataframe==1] = np.nan

        # Return
        return self


    def plot(self, organisms=None, antibiotics=None,
                                 genera=None,
                                 categories=None,
                                 method='weighted',
                                 metric='euclidean',
                                 vmin=0.0,
                                 vmax=1.0,
                                 cmap=None,
                                 figsize=(5,5),
                                 xticklabels=True,
                                 yticklabels=True,
                                 **kwargs):
        """This function plots the antibiogram.

        The arguments are those to be passed to the clustermap implementation
        which is available on seaborn.

        Parameters
        ----------
        method: string-like

        metric: string-like

        vmin, vmax: float-like, float-like
          The min and maximum values within the matrix (or feasible range).

        cmap: string-like
          The colormap to be used to plot the resistance indexes.

        figsize: tuple-like
          The size of the figure

        Returns
        -------
        an axis object
        """
        # Define colormap
        if cmap is None:
          cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

        # Copy dataframe
        dataframe = self._dataframe.copy(deep=True)

        # Filter data
        if organisms is not None:
          dataframe = dataframe.loc[_idxs(dataframe.index, 0, organisms), :]
        if genera is not None:
          dataframe = dataframe.loc[_idxs(dataframe.index, 1, genera), :]
        if antibiotics is not None:
          dataframe = dataframe.loc[:, _idxs(dataframe.columns, 0, antibiotics)]
        if categories is not None:
          dataframe = dataframe.loc[:, _idxs(dataframe.columns, 1, categories)]

        # Create mask
        mask = pd.isnull(dataframe)

        # Fill nan with a very small value
        dataframe = dataframe.fillna(1e-10)

        # Get values for groups
        rows = dataframe.index.get_level_values(1).values
        cols = dataframe.columns.get_level_values(1).values

        # Get colors
        row_colors = _get_category_colors(rows, self.colormap_genus)
        col_colors = _get_category_colors(cols, self.colormap_category)

        # Create series with index (for clustermap)
        row_colors = pd.Series(row_colors.values, index=dataframe.index)
        col_colors = pd.Series(col_colors.values, index=dataframe.columns)

        # Plot clustermap
        grid = sns.clustermap(dataframe, center=0.5,
          method=method, metric=metric, vmin=vmin, vmax=vmax, mask=mask,
          cmap=cmap, linewidths=.75, figsize=figsize, xticklabels=True,
          yticklabels=True, row_colors=row_colors, col_colors=col_colors,
          **kwargs)

        # Format labels names
        labelsx = ['(%s) %5s' % (e.get_text().split('-')[1],
                                 e.get_text().split('-')[0])
                        for e in grid.ax_heatmap.get_xticklabels()]
        labelsy = ['%-6s (%s)' % (e.get_text().split('-')[0],
                                 e.get_text().split('-')[1])
                         for e in grid.ax_heatmap.get_yticklabels()]

        # Set labels names
        grid.ax_heatmap.set_xticklabels(labelsx)
        grid.ax_heatmap.set_yticklabels(labelsy, rotation=0)
        #grid.ax_heatmap.set_aspect('equal')

        # Format figure
        plt.suptitle('Antibiogram (%s, %s)' % (metric.lower(),method.lower()))
        plt.subplots_adjust(bottom=0.3, top=0.9, left=0.05, right=0.7)

        # Return
        return grid







if __name__ == '__main__':

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


    # -------------------------------------------------------------------------
    #                                main
    # -------------------------------------------------------------------------
    # Data path.
    path = '../fixtures/fixture_antibiogram.csv'

    # -------------------------------
    # Load data
    # -------------------------------
    # Load
    dataframe = pd.read_csv(path)

    # -------------------------------
    # Create object
    # -------------------------------
    # Antibiogram plotter
    antibiogram = Antibiogram(column_organism='organismCode',
                              column_antibiotic='antibioticCode',
                              column_genus='specieName',
                              column_category='antibioticClass',
                              column_index='sari')

    # Fit antibiogram
    antibiogram = antibiogram.fit(dataframe)

    # ---------
    # Example 1
    # ----------
    antibiogram.plot(organisms=['ECOL', 'SAUR'], figsize=(15, 3))


    # ---------
    # Example 2
    # ---------
    antibiogram.plot(genera=['staphylococcus',
                             'klebsiella',
                             'streptococcus',
                             'enterococcus',
                             'enterobacter'],
                     categories=None,
                     method='weighted',
                     metric='euclidean',
                     figsize=(16, 9))

    # Show
    # plt.show()