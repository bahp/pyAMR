"""
Table Scatterplot
=================

"""
# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib import colors

# Own libraries
from pyamr.utils.plot import MidpointNormalize
from pyamr.utils.plot import vlinebgplot
from pyamr.graphics.table_graph import _DEFAULT_CONFIGURATION

# -------------------------------------------
# Main
# -------------------------------------------

# Create data
data = [
    [9, 'SAUR', 'TRI',  0.720,  0.100,  0.274, 0.112,  0.056,  0.000,  0.0,   -0.046,  7.189],
    [8, 'SAUR', 'MUP',  0.084,  0.025, -0.007, 0.009,  0.064,  0.429,  0.0,   -0.499,  7.230],
    [7, 'SAUR', 'ERY',  0.082,  0.260, -0.007, 0.092,  0.123,  0.414,  0.0,   -0.526,  8.604],
    [6, 'SAUR', 'CLI',  0.058,  0.224, -0.016, 0.033,  0.099,  0.653,  0.0,   -0.468,  8.602],
    [5, 'SAUR', 'RIF', -0.093,  0.017, -0.008, 0.056,  0.043,  0.436,  0.0,    0.217,  7.545],
    [4, 'SAUR', 'PEN', -0.120,  0.894,  0.086, 0.262,  0.168,  0.022,  0.0,    0.439,  8.588],
    [0, 'SAUR', 'CIP', -0.480,  0.200,  0.166, 0.545,  0.100,  0.002,  0.0,   -0.795,  7.562],
    [1, 'SAUR', 'FUS', -0.480,  0.146,  0.094, 0.221,  0.038,  0.017,  0.0,   -0.033,  8.592],
    [2, 'SAUR', 'MET', -0.480,  0.153,  0.174, 0.144,  0.090,  0.002,  0.0,   -0.621,  8.599],
    [3, 'SAUR', 'TET', -0.480,  0.098,  0.184, 0.125,  0.045,  0.001,  0.0,    0.215,  7.606]
]

# Create dataframe
data = pd.DataFrame(data, columns=['idx', 'org', 'abx',
    'sart_m', 'sari', 'r2', 'jb', 'dw', 'ptm', 'ptn',
    'pearson', 'percent'])

# Show
print("\nData:")
print(data)

# Filter features
data = data[data.columns[2:]]

# -------------------------------------------
# Pair Grid
# -------------------------------------------
# Create plotting configuration
info = _DEFAULT_CONFIGURATION
info['percent'] = {
    'name': 'percent',
    'cmap': 'Blues',
    'title': 'Percent',
    'xlim': [7, 9],
    'xticks': [7, 9],
    'vline': [],
}

# Create pair grid
g = sns.PairGrid(data, x_vars=data.columns[1:],
        y_vars=["abx"], height=3, aspect=.45)

# Draw a dot plot using the stripplot function
# g.map(sns.stripplot, size=10, orient="h", jitter=False,
#      palette="flare_r", linewidth=1, edgecolor="w")

# Set common features
g.set(xlabel='', ylabel='')

# Plot strips and format axes
for ax, c in zip(g.axes.flat, data.columns[1:]):

    # Get information
    d = info[c] if c in info else {}

    # Display
    # sns.stripplot(data=data, x=title, y='abx', size=10,
    #    orient="h", jitter=False, linewidth=0.75, ax=ax,
    #    edgecolor="gray", palette=d.get('cmap', None))
    #    color='b')

    # .. note: We need to use scatter plot if we want to
    #          assign colors to the markers according to
    #          their value.

    # Using scatter plot
    sns.scatterplot(data=data, x=c, y='abx', s=100, alpha=1,
                    ax=ax, linewidth=0.75, edgecolor='gray',
                    c=data[c], cmap=d.get('cmap', None),
                    norm=d.get('norm', None))

    # Plot vertical lines
    for e in d.get('vline', []):
        vlinebgplot(ax, top=data.shape[0], **e)

    # Configure axes
    ax.set(title=d.get('title', c),
           xlim=d.get('xlim', None),
           xticks=d.get('xticks', []),
           xlabel='', ylabel='')
    ax.tick_params(axis='y', which='both', length=0)
    ax.xaxis.grid(False)
    ax.yaxis.grid(visible=True, which='major',
                  color='gray', linestyle='-', linewidth=0.35)
    ax.set_axisbelow(True)

# Despine
sns.despine(left=True, bottom=True)

# Adjust layout
plt.tight_layout()

# Show
plt.show()