# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl

from matplotlib import colors


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


# -----------------------------------------------------------------
#                           Methods
# -----------------------------------------------------------------
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


def vlinebgplot(ax, top, xv, bg=None):
    """This function adds a vertical line and background

    Parameters
    ----------
    ax: matplotlib axes
    top: float
        The max y value
    xv: float
        The x value
    bg: boolean
        Whether to include a background

    Returns
    -------
    """
    # Libraries
    import seaborn as sns

    # Plot line.
    ax.plot((xv, xv), (-1, top), color='gray',
            linestyle='--', linewidth=1, zorder=0)

    # Plot background.
    if bg is not None:
        cb = sns.color_palette("Set2", 10)[1]
        ax.fill_between([xv, bg], [-1, -1], [top, top],
                        zorder=0, alpha=0.1, color=cb)


def hlinebgplot(ax, right, yv, bg=None):
    """This function adds a vertical line and background

    Parameters
    ----------

    Returns
    -------
    """
    # Libraries
    import seaborn as sns

    # Plot line
    ax.plot((-1, right), (yv, yv), color='gray',
            linestyle='--', linewidth=1, zorder=0)

    # Plot background.
    if bg is not None:
        cb = sns.color_palette("Set2", 10)[1]
        ax.fill_between([-1, right], [yv, yv], [bg, bg],
                        zorder=0, alpha=0.2, color=cb)


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


class MidpointNormalize(colors.Normalize):
    """
    Normalise the colorbar so that diverging bars work their way
    either side from a prescribed midpoint value)

    Example
    -------
        > MidpointNormalize(midpoint=0., vmin=-100, vmax=100)

    """

    def __init__(self, vmin=None,
                       vmax=None,
                       midpoint=None,
                       clip=False):
        """Constructor
        """
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        """Call

        .. note: Ignoring masked values and all kind of edge cases
                 to keep it simple.
        """
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin,
                self.midpoint,
                self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))