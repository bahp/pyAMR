"""
Table Boxplot
=============

"""
# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib import colors

from pyamr.graphics.utils import hlinebgplot


# -------------------
# PLOTTING SETTINGS
# -------------------
# Configuration for each columns
info_sari = {
  'cmap':'Reds',
  'title':'SARI',
  'xlim':[-0.1, 1.1],
  'xticks':[0, 1],
}

info_sart = {
  'cmap':'RdBu_r',
  'title':'SART',
  'xlim':[-1.2, 1.2],
  'xticks':[-1, 1],
}

info_r2 = {
  'cmap':'YlGn',
  'title':'R2',
  'ylim': [-0.2, 1.2],
  'yticks': [.0, .2, .4, .6, .8 ]
}

info_fprob = {
  'name':'f_prob',
  'title':'Prob(F)',
  'ylim': [-0.2, 1.2],
  'yticks': [.0, .2, .4, .6, .8 ]
}

info_jb_prob = {
  'cmap':'YlGn',
  'title':'Prob(JB)',
  'ylim': [-0.2, 1.2],
  'hline': [{'yv':0.05, 'bg':0.0}],
  'yticks': [.0, .2, .4, .6, .8 ]
}

info_dw = {
  'cmap':'YlGn_r',
  'title':'DW',
  'hline': [{'yv':0.8, 'bg':4.0}],
  'ylim': [-0, 4.2],
  'yticks': [1, 2, 3]
}

info_slope = {
  'name':'x1_tprob',
  'cmap':'YlGn_r',
  'title':'P>|t| m',
  'hline': [{'yv':0.05, 'bg':1.0}],
  'ylim': [-0.2, 1.2],
  'yticks': [.0, .2, .4, .6, .8 ]
}

info_coefficient = {
  'name':'c_tprob',
  'cmap':'YlGn_r',
  'title':'P>|t| n',
  'hline': [{'yv':0.05, 'bg':1.0}],
  'ylim': [-0.2, 1.2],
  'yticks': [.0, .2, .4, .6, .8 ]
}


# Now we combine all of them together. Note
# that the key value corresponds to the name
# of the column it should be applied to.
info = {
    'sari': info_sari,
    'sart': info_sart,
    'dw': info_dw,
    'r2': info_r2,
    'jb_prob': info_jb_prob,
    'ptm': info_slope,
    'ptn': info_coefficient,
    'f_prob': info_fprob
}

# -------------------------------------------
# Main
# -------------------------------------------
# Data path.
path = '../../pyamr/fixtures/fixture_surveillance.csv'

# Rename
rename = {
    'organismCode': 'org',
    'antibioticCode': 'abx',
    'sari': 'sari',
    'x1_coef': 'sart',
    'adj_rsquared': 'r2',
    'f_prob': 'f_prob',
    'jarque-bera': 'jb',
    'jarque_bera_prob': 'jb_prob',
    'x1_tprob': 'ptm',
    'c_tprob': 'ptn',
    'durbin-watson': 'dw',
    'surveillance': 'surveillance'
}

# Create data
data = pd.read_csv(path)
data = data[rename.keys()]
data = data.rename(columns=rename)

# Show
print("\nData:")
print(data)


# -------------------------------------------
# Pair Grid
# -------------------------------------------
# Features
statistics = ['r2', 'f_prob', 'jb_prob', 'ptm', 'ptn', 'dw']

# Create figure
f, axes = plt.subplots(1, len(statistics), figsize=(12, 3))
axes = axes.flatten()

# Plot strips and format axes
for ax, c in zip(axes, statistics):

    # Get information
    d = info[c] if c in info else {}

    # Plot distributions
    sns.boxplot(x='surveillance', y=data[c],
                ax=ax, data=data, whis=1e30,
                palette="Set3", linewidth=0.75)

    # Plot horizontal lines
    for e in d.get('hline', []):
        hlinebgplot(ax, right=3, **e)

    # Configure axes
    ax.set(title=d.get('title', c),
           xlabel='', ylabel='',
           ylim=d.get('ylim', None),
           yticks=d.get('yticks', ax.get_yticks()))
    #ax.tick_params(axis='y', which='both', length=0)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)

# Despine
sns.despine(bottom=True, left=True)

# Change last ticks to right
axes[-1].yaxis.tick_right()

# Adjust space (overwritten by tight)
plt.subplots_adjust(wspace=0.75)

# Configure layout
#plt.tight_layout()

# Show
plt.show()