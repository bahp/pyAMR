# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl


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

# ------------------------
# Methods
# ------------------------
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



def get_category_colors(index, category, cmap='hls'):
    """Creates the colors for the different elements in
    a given categorical feature vector.

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
    pd.Series
        List of colors.
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


def plot_sns_heatmap():
    pass


def plot_sns_clustermap():
    pass


def plot_sns_relmap():
    pass


def plot_spectrum():
    pass


def plot_timeseries():
    pass