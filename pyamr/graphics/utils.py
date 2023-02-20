# Libraries
import numpy as np
from matplotlib import colors

class MidpointNormalize(colors.Normalize):
    """Normalise the colorbar so that diverging bars
       work there way either side from a prescribed
       midpoint value)

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
    # Library
    import matplotlib as mpl
    import seaborn as sns

    # Create scalar mappable
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    # Gete color map
    colormap = sns.color_palette([mapper.to_rgba(i) for i in values])
    # Return
    return colormap