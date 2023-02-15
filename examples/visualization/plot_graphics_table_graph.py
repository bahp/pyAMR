"""
Graphics TableGraph example
============================
"""
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

from pyamr.graphics.table_graph import TableGraph

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
dataframe.columns = ['c0', 'c1', 'c2']

# Show
print("\nData:")
print(dataframe)

# Create column configurations
c0 = TableGraph().get_map_config(title='Column 0', cmap='Reds')
c2 = TableGraph().get_map_config(title='Column 2', cmap='RdBu_r',
                                 midpoint=50, xticks=[20, 40, 60, 80],
                                 xline=[{'xv': 25, 'bg': 0}, {'xv': 75, 'bg': 100, 'cb': 'y'}])

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