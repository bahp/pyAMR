###############################################################################
# Author: Bernard Hernandez
# Filename:
# Date: 
# Description:
#
###############################################################################

# Libraries
import os
import sys
import json
import copy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec

from scipy import interp
from matplotlib.colors import ListedColormap

# Own
from pyamr.graphics.utils import MidpointNormalize
from pyamr.graphics.utils import vlinebgplot


# ------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------
# These are some pre-defined configurations to facilitate the display
# of some common statistics (R2, jarque-bera, skew) and amr metrics
# (sari, sart, ...) computed in this library.

_DEFAULT_KWGS = {
    'name':'sari',
    'cmap':'Reds',
    'title':'SARI',
    'xlim':[-0.1, 1.1],
    'xticks':[0, 1],
    'kwargs': {
        's':80,
        'vmin':0,
        'vmax':1
    }
}

# Configuration for each columns
_DEFAULT_SARI = {
    'cmap': 'Reds',
    'title': 'SARI',
    'xlim': [-0.1, 1.1],
    'xticks': [0, 1],
    'norm': colors.Normalize(vmin=0, vmax=1),
}

_DEFAULT_SARI_PCT = {
    'cmap': 'Reds',
    'title': 'SARI (%)',
    'xlim': [-1, 101],
    'xticks': [0, 100],
    'norm': colors.Normalize(vmin=0, vmax=100),
}

_DEFAULT_SARI_LR = {
    'cmap': 'Reds',
    'title': 'SARI-lr',
    'xlim': [-0.1, 1.1],
    'xticks': [0, 1],
    'norm': colors.Normalize(vmin=0, vmax=1),
}

_DEFAULT_SART_M = {
    'cmap': 'RdBu_r',
    'title': 'SART (m)',
    'xlim': [-1.2, 1.2],
    'xticks': [-1, 1],
    'norm': colors.Normalize(vmin=-1, vmax=1),
}

_DEFAULT_SART_Y = {
    'cmap': 'RdBu_r',
    'title': 'SART (y)',
    'xlim': [-1.2, 1.2],
    'xticks': [-1, 1],
    'norm': colors.Normalize(vmin=-1, vmax=1),
}

_DEFAULT_R2 = {
    'cmap': 'YlGn',
    'title': 'R2',
    'xlim': [-0.15, 1.1],
    'xticks': [0, 1],
    'norm': colors.Normalize(vmin=0, vmax=1),
}

_DEFAULT_R2ADJ = {
    'cmap': 'YlGn',
    'title': 'R2 Adj',
    'xlim': [-0.15, 1.1],
    'xticks': [0, 1],
    'norm': colors.Normalize(vmin=0, vmax=1),
}

_DEFAULT_JB = {
    'cmap': 'YlGn',
    'title': 'Prob(JB)',
    'xlim': [-0.1, 1.1],
    'xticks': [0, 1],
    'vline': [{'xv': 0.05, 'bg': -0.1}],
    'norm': colors.Normalize(vmin=0, vmax=1),
}

_DEFAULT_JB_PROB = {
    'cmap': 'YlGn',
    'title': 'Prob(JB)',
    'xlim': [-0.1, 1.1],
    'xticks': [0, 1],
    'vline': [{'xv': 0.05, 'bg': -0.1}],
    'norm': colors.Normalize(vmin=0, vmax=1),
}

_DEFAULT_DW = {
    'cmap': 'YlGn_r',
    'title': 'DW',
    'xlim': [-0.4, 4.4],
    'xticks': [0, 2, 4],
    'vline': [{'xv': 0.8, 'bg': 4.4}],
    'norm': colors.Normalize(vmin=0, vmax=4),
}

_DEFAULT_FREQ = {
    'cmap': 'Blues',
    'title': 'Freq',
    'xticks': [0, 40000, 80000],
    'kwargs': {
        's': 80,
        'vmin': 0
    }
}

_DEFAULT_PEARSON = {
    'cmap': 'Reds',
    'title': 'Pearson',
    'xlim': [-1.1, 1.1],
    'xticks': [-1, 0, 1],
    'vline': [{'xv': -0.5, 'bg': -1.1},
              {'xv': 0.5, 'bg': 1.1}],
    'norm': colors.Normalize(vmin=-1, vmax=1),
}

_DEFAULT_KENDALL = {
    'cmap': 'Reds',
    'title': 'Kendall',
    'xlim': [-1.1, 1.1],
    'xticks': [-1, 0, 1],
    'vline': [{'xv': -0.5, 'bg': -1.1},
              {'xv': 0.5, 'bg': 1.1}],
    'norm': colors.Normalize(vmin=-1, vmax=1),
}

_DEFAULT_SPEARMAN = {
    'cmap': 'Reds',
    'title': 'Spearman',
    'xlim': [-1.1, 1.1],
    'xticks': [-1, 0, 1],
    'vline': [{'xv': -0.5, 'bg': -1.1},
              {'xv': 0.5, 'bg': 1.1}],
    'norm': colors.Normalize(vmin=-1, vmax=1),
}

_DEFAULT_SKEW = {
    'cmap': 'Reds',
    'title': 'Skew',
    'xticks':[0],
    'vline': [{'xv': 0}]
}

_DEFAULT_KURTOSIS = {
    'cmap': 'Reds',
    'title': 'Kurtosis',
    'xticks':[3],
    'vline': [{'xv': 3}]
}

_DEFAULT_OMNIBUS = {
    'cmap': 'Reds',
    'title': 'Omnibus',
    'vline': [{'xv': 0.05, 'bg': 1.1}],
    'norm': colors.Normalize(vmin=-1, vmax=1),
}

_DEFAULT_SLOPE = {
    'name': 'x1_tprob',
    'cmap': 'YlGn_r',
    'title': 'P>|t| m',
    'xlim': [-0.1, 1.1],
    'xticks': [0, 1],
    'vline': [{'xv': 0.05, 'bg': 1.1}],
    'norm': MidpointNormalize(vmin=0, vmax=1, midpoint=0.5),
}

_DEFAULT_COEFFICIENT = {
    'name': 'c_tprob',
    'cmap': 'YlGn_r',
    'title': 'P>|t| n',
    'xlim': [-0.1, 1.1],
    'xticks': [0, 1],
    'vline': [{'xv': 0.05, 'bg': 11.1}],
    'norm': MidpointNormalize(vmin=0, vmax=1, midpoint=0.5),
}

_DEFAULT_PERCENT = {
    'name': 'percent',
    'cmap': 'Blues',
    'title': 'Percent',
    'xlim': [7, 9],
    'xticks': [0, 100],
    'vline': [],
}

# Now we combine all of them together. Note
# that the <key> value corresponds to the name
# of the column it should be applied to.
_DEFAULT_CONFIGURATION = {
    'sari': _DEFAULT_SARI,
    'sari_pct': _DEFAULT_SARI_PCT,
    'sart_m': _DEFAULT_SART_M,
    'sart_y': _DEFAULT_SART_Y,
    'dw': _DEFAULT_DW,
    'r2': _DEFAULT_R2,
    'r2_adj': _DEFAULT_R2ADJ,
    'pearson': _DEFAULT_PEARSON,
    'jb': _DEFAULT_JB,
    'jb_prob': _DEFAULT_JB_PROB,
    'percent': _DEFAULT_PERCENT,
    'ptm': _DEFAULT_SLOPE,
    'ptn': _DEFAULT_COEFFICIENT,
    'omnibus': _DEFAULT_OMNIBUS,
    'kurtosis': _DEFAULT_KURTOSIS,
    'skew': _DEFAULT_SKEW,
    'freq': _DEFAULT_FREQ
}






class TableGraph:
    """"""
    # Attributes
    fontsize = 9

    # ---------------------------------------------------------------------------
    #                              HELPER METHODS
    # ---------------------------------------------------------------------------
    def get_map_config(self, title=None,
                             xlim=None,
                             xsym=False,
                             xticks=None,
                             xline=[],
                             vmin=None,
                             vmax=None,
                             vsym=False,
                             cmap='Blues',
                             midpoint=None,
                             s=80,
                             linewidths=0.75,
                             edgecolor='gray',
                             **kwargs):
        """This function helps creating a configuration map.
        """
        # Create new map.
        return { 'ax_kwargs': {
                   'title':title,
                   'xlim':xlim,
                   'xsym':xsym,
                   'xticks':xticks,
                   'xline':xline,
                 },
                 'cmap_kwargs': {
                   'vmin':vmin,
                   'vmax':vmax,
                   'vsym':vsym,
                   'cmap':cmap,
                   'midpoint':midpoint
                 },
                 'scatter_kwargs': {
                   's':s,
                   'linewidths':linewidths,
                   'edgecolor':edgecolor
                 }
               }

    def _init_axes(self, ncolumns):
        """This method initialises the axes.

        Parameters
        ----------
        ncolumns : number of columns.

        Returns
        -------
        axes : array with the corresponding axes.
        """
        # Create grid spec.
        gs = gridspec.GridSpec(1, ncolumns)
        gs.update(left=0.15,
                  right=0.97,
                  bottom=0.12,
                  top=0.85,
                  wspace=0.15)
        # Create subplots.
        return [plt.subplot(gs[j]) for j in range(ncolumns)]

    def _init_conf(self, ncolumns, configuration={},
                                 column_names=None):
        """This method initialises the configuration parameters.

        Parameters
        ----------
        ncolumns      :
        configuration :
        column_names  :

        Returns
        -------
        """
        # Create array with configuration parameters
        v_configuration = []
        # For each column.
        for i in range(ncolumns):
            # Get default configuration.
            config = self.get_map_config()
            # Configuration labelled with an index.
            if i in configuration.keys():
                config.update(configuration[i])
            # Configuration labelled with a name.
            if column_names[i] in configuration.keys():
                config.update(configuration[column_names[i]])
            # Append
            v_configuration.append(config)
        # Return it.
        return v_configuration


    def _vmin_vmax(self, x=None, vmin=None, vmax=None, vsym=True):
        """This function finds the vmin and vmax.

        Parameters
        ----------
        x    : array with values.
        vmin : manually selected vmin.
        vmax : manually selected vmax.

        Returns
        -------
        vmin : the minimum value.
        vmax : the maximum value.
        """
        # Find maximum and minimum.
        if vmin is None: vmin = min(x)
        if vmax is None: vmax = max(x)
        # Symmetric
        if vsym:
            if abs(vmin)>abs(vmax):
                lim = abs(vmin)
            else:
                lim = abs(vmax)
            vmin, vmax = -lim, lim
        # Return
        return vmin, vmax

    def _colormap_info(self, x, cmap='Blues', vmin=None,
                                            vmax=None,
                                            vsym=None,
                                            midpoint=None):
        """This function computes the colormap.

        Parameters
        ----------
        name     : the name of the colormap.
        vmin     : the minimum value to assign a color.
        vmax     : the maximum value to assign a color.
        vsym     : have same color scale when vmin and vmax are not the same.
        midpoint : the midpoint for a cmap with diverging colors.

        Returns
        -------
        colormap : the desired values to pass to scatter.
        """
        # Find vmin and vmax.
        vmin, vmax = self._vmin_vmax(x, vmin, vmax, vsym)
        # Compute basic colormap.
        if isinstance(cmap, str):
            cmap = ListedColormap(sns.color_palette(cmap, len(x)))
        # Compute midpoint colormap.
        if midpoint is not None:
            norm = MidpointNormalize(midpoint=midpoint,
                                     vmin=vmin,
                                     vmax=vmax)
        else:
            norm = None

        # Return
        return x, vmin, vmax, cmap, norm

    # ---------------------------------------------------------------------------
    #                               AXIS METHODS
    # ---------------------------------------------------------------------------
    def _configure_axis(self, x, ax, title=None,
                                   xlim=None,
                                   xsym=False,
                                   xticks=None,
                                   xline=[]):
        """This method configures the axis given external information.

        Parameters
        ----------
        ax : axes to configure.

        Returns
        -------
        ax : the axis that has been modified.
        """
        # Aux variable
        y = np.arange(len(x))
        # Format axis.
        ax.set_yticks(y)                  # Set y ticks.
        ax.set_ylim([-1, len(y)])         # Y axis limit.
        ax.set_facecolor((1, 1, 1))       # Change the background color.
        ax.yaxis.grid(visible=True, which='major', # Create grid with horizontal lines.
                              color='gray',
                              linestyle='-',
                              linewidth=0.35)
        ax.xaxis.grid(visible=True, which='major', # Create grid with horizontal lines.
                              color='gray',
                              linestyle='--',
                              linewidth=0.35)

        # Hide y-labels.
        for j,e in enumerate(ax.get_yticklabels()): # Hide ylabels.
            plt.setp(e, visible=False)

        # Hide all spines.
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Basic configuration
        if title is not None:  ax.set_title(title)
        if xticks is not None: ax.set_xticks(xticks)
        if xlim is not None:
            vmin, vmax = self._vmin_vmax(vmin=xlim[0], vmax=xlim[1], vsym=xsym)
            ax.set_xlim([vmin, vmax])

        # Add vertical lines.
        for v in xline:
            self.plot_vertical_line(ax, top=len(y)+1, **v)


    def plot_vertical_line(self, ax, top, xv, bg=None, lw=1.0, cb=None):
        """This function adds a vertical line and background

        Parameters
        ----------
        ax  : the axis to plot the line.
        top : the height of the vertical line.
        xv  : the x value where the line should be placed.
        bg  : the x value where the background should be extended.

        Returns
        -------
        """
        # Plot line.
        ax.plot((xv,xv),(-1,top), color='gray',
                                  linestyle='--',
                                  linewidth=lw,
                                  zorder=0)

        # Plot background.
        if bg is not None:
            if cb is None:
                cb = sns.color_palette("Set2", 10)[1]
            ax.fill_between([xv,bg], [-1,-1], [top,top], zorder=0,
                                                   alpha=0.1,
                                                   color=cb)

    def plot_array(self, x, ax=None, ax_kwargs={},
                                   cmap_kwargs={},
                                   scatter_kwargs={},
                                   **kwargs):
        """this method plots a single column.

        Parameters
        ----------
        x              : values to plot.
        ax             : axis to plot the information.
        ax_kwargs      : axis configuration information.
        cmap_kwargs    : cmap configuration information.
        scatter_kwargs : scatter configuration information.

        Returns
        -------
        axis : the axis in which the series is plotted.
        """
        # Create ax if it is not passed.
        if ax is None:
          f, ax = plt.subplots()
        # Create colormap.
        c, vmin, vmax, cmap, norm = self._colormap_info(x, **cmap_kwargs)
        if norm is not None:
            ax.scatter(x=x, y=np.arange(len(x)), c=c,
                       cmap=cmap, norm=norm, **scatter_kwargs)
        else:
            ax.scatter(x=x, y=np.arange(len(x)), c=c,
                       vmin=vmin, vmax=vmax, cmap=cmap,
                       norm=norm, **scatter_kwargs)
        # Configure axis.
        self._configure_axis(x=x, ax=ax, **ax_kwargs)
        # Return axis
        return ax


    def plot_matrix(self, data, axes=None,
                              ylabels=None,
                              clabels=None,
                              configuration={}):
        """This method plots a matrix.

        Parameters
        ----------
        data          :
        ylabels       :
        configuration :
        """
        # Create figure.
        plt.figure()

        # Set style.
        sns.set(style="whitegrid")

        # Get labels.
        ylabels = range(data.shape[0]) if ylabels is None else ylabels
        clabels = range(data.shape[1]) if clabels is None else clabels

        # Initialise the axes.
        if axes is None:
          axes = self._init_axes(data.shape[1])

        # Initliaise the configuration maps.
        conf = self._init_conf(ncolumns=data.shape[1],
                               configuration=configuration,
                               column_names=clabels)

        # Loop and display each column.
        for i, (x,ax,cf) in enumerate(zip(data.T, axes, conf)):
          ax = self.plot_array(x=x, ax=ax, **cf)

        # Set ylabels.
        axes[0].set_yticklabels(ylabels)

        # Show ylabels.
        ticks = axes[0].get_yticklabels()
        for j,e in enumerate(ticks):
            plt.setp(e, visible=True)

        # Set clabels.
        for ax,label in zip(axes,clabels):
          if ax.get_title()=='':
            ax.set_title(label)

        # Return
        return axes



    def plot_dataframe(self, dataframe, axes=None, configuration={}):
        """This method plots the whole table.

        Parameters
        ----------
        dataframe     :
        configuration :

        Returns
        -------
        """
        # Get ylabels and clabels.
        clabels = dataframe.columns.values
        ylabels = dataframe.index.values

        # Convert as matrix.
        if isinstance(dataframe, pd.DataFrame):
          data = dataframe.to_numpy()

        # Plot matrix
        return self.plot_matrix(data, ylabels=ylabels,
                                      clabels=clabels,
                                      axes=axes,
                                      configuration=configuration)


    def plot(self, data, **kwargs):
        """
        """
        if isinstance(data, pd.DataFrame):
          return self.plot_dataframe(dataframe=data, **kwargs)
        if isinstance(data, pd.Series):
          return self.plot_dataframe(dataframe=data.to_frame(), **kwargs)
        if isinstance(data, np.ndarray):
          return self.plot_matrix(data=data, **kwargs)






if __name__ == '__main__':

  """
  
     Example of axis configuration
     -----------------------------
    { 'ax': None,
      'ax_kwargs': {
        'title':'Example 1',
        'xlim':None,
        'xsym':False,
        'xticks':None,
        'xline':[{'xv':0.05, 'bg':-1.0, 'cb':'y'}],
      },
      'cmap_kwargs': {
        'vmin':None,
        'vmax':None,
        'vsym':False,
        'cmap':'RdBu_r',
        'midpoint':2.5
      },
      'scatter_kwargs': { 
        's':80, 
        'linewidths':0.75,
        'edgecolor':'gray'
      }
    }
  """

  # Create data
  data = np.random.randint(100, size=(20, 3))
  dataframe = pd.DataFrame(data)
  dataframe.columns = ['c0','c1','c2']

  # Show
  print("\nData:")
  print(dataframe)

  # Create column configurations
  c0 = TableGraph().get_map_config(title='Column 0', cmap='Reds')
  c2 = TableGraph().get_map_config(title='Column 2', cmap='RdBu_r',
        midpoint=50, xticks=[20,40,60,80],
        xline=[{'xv':25, 'bg':0}, {'xv':75, 'bg':100, 'cb':'y'}])

  # Create configuration
  config = {}
  config['c0'] = c0
  config[2] = c2

  # Example with a DataFrame
  axes = TableGraph().plot(data=dataframe, configuration=config)

  # Example with numpy array
  axes = TableGraph().plot(data=data, configuration=config)

  # Show.
  plt.show()











class TableGraph2:

  def check_vmin_vmax(self, x, kwargs):
    """This methos check the vmax and vmin for colors.

    Parameters
    ----------

    Returns
    -------
    """
    # Check if there is min and max.
    ismin = 'vmin' in kwargs
    ismax = 'vmax' in kwargs
    # Add to kwargs
    if ismin and ismax: return kwargs
    if ismin and not ismax: kwargs['vmax'] = x.max() 
    if ismax and not ismin: kwargs['vmin'] = x.min()
    if not ismin and not ismax:
      if abs(x.max())>abs(x.min()): 
        l=abs(x.max())
      else:
        l=abs(x.min())
      kwargs['vmin'] = -l
      kwargs['vmax'] = l
    # Return 
    return kwargs


  def add_vline(self, ax, top, xv, bg=None):
    """This function adds a vertical line and background

    Parameters
    ----------

    Returns
    -------
    """
    # Plot line.
    ax.plot((xv,xv),(-1,top), color='gray', 
                              linestyle='--', 
                              linewidth=1,
                              zorder=0)
 
    # Plot background.
    if bg is not None:
      cb = sns.color_palette("Set2", 10)[1]
      ax.fill_between([xv,bg], [-1,-1], [top,top], zorder=0,  
                                                   alpha=0.1, 
                                                   color=cb)
  



  def display_column(self, x, y, cmap, ax, **kwargs):
    """This method displays a single column.

    Parameters
    ----------

    Returns
    -------
    """
    # Check if there is maximum and minimum.
    kwargs = self.check_vmin_vmax(x, kwargs)

    # Normalize colormap.
    if 'cmap_midpoint' in kwargs:
      kwargs['norm'] = \
       MidpointNormalize(midpoint=kwargs['cmap_midpoint'], 
                         vmin=kwargs['vmin'], 
                         vmax=kwargs['vmax'])
      del kwargs['cmap_midpoint']


    # Plot.
    ax.scatter(x=x, 
               y=y, 
               c=x, 
               cmap=cmap,
               edgecolor='gray',
               **kwargs)

    # Configure axis generic.
    ax.set_ylim([-1, len(y)])
    ax.set_xticks([])
    ax.set_yticks(range(len(y)))

    # Common for all.
    #ax.set_axis_bgcolor((1, 1, 1))
    ax.yaxis.grid(visible=True, which='major',
                          color='gray', 
                          linestyle='-',
                          linewidth=0.35)

    # Hide ylabels.
    ticks = ax.get_yticklabels()
    for j,e in enumerate(ticks):
        plt.setp(e, visible=False)


  def plot(self, df, axes, information):
    """This method plots the whole table.

    Parameters
    ----------

    Returns
    -------
    """
    # Set style.
    sns.set(style="whitegrid")
    
    # Loop and display.
    for ax,info in zip(axes,information):
      # Get values.
      x = df[info['name']]
      y = df.index.values
      c = ListedColormap(sns.color_palette(info['cmap'], len(df)))

      # Display column
      self.display_column(x=x, y=y, cmap=c, ax=ax, **info['kwargs'])

      # Basic config.
      if 'title' in info: 
        ax.set_title(info['title'])
      if 'vline' in info:
        for e in info['vline']:
          self.add_vline(ax, top=len(y)+1, **e)
      if 'xlim' in info:
        ax.set_xlim(info['xlim'])
      if 'xticks' in info:
        ax.set_xticks(info['xticks'])

    # Set ylabels.
    #organisms = df['organismCode']   # np.flip(x, axis=0)
    #antibiotics = df['antibioticCode']
    #labels = ["(%-5s,%5s)"%(o,a) for o,a in zip(organisms, antibiotics)]

    #labels = df['antibioticCode']
    #axes[0].set_yticklabels(labels)

    # Show ylabels.
    ticks = axes[0].get_yticklabels()
    for j,e in enumerate(ticks):
        plt.setp(e, visible=True)

    # Return
    return axes


