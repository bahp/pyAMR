# Division
from __future__ import division

# Generic libraries
import os
import sys
import warnings
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# Import own module
sys.path.append('../../../')

# Import specific
from pyamr.datasets import load

mpl.rcParams['font.size'] = 6
# -----------------------------------------------------------------------
#
# -----------------------------------------------------------------------

"""
# Load microbiology
microbiology = load.dataset_epicimpoc_susceptibility()
microbiology = microbiology.replace(\
  {'orderCode': {'WOUND CULTURE': 'WOUCUL',
                 'URINE CULTURE': 'URICUL',
                 'SPUTUM CULTURE': 'SPTCUL',
                 'BLOOD CULTURE': 'BLDCUL'}})

# Group by culture code and count
microbiology_count = microbiology.groupby(by=['orderCode', 'antibioticCode']).size()
microbiology_count = microbiology_count.sort_values(ascending=False)
microbiology_count = microbiology_count.reset_index()

print microbiology_count[microbiology_count['orderCode']=='URICUL']
print microbiology_count[microbiology_count['orderCode']=='WOUCUL']
print microbiology_count[microbiology_count['orderCode']=='SPTCUL']
print microbiology_count[microbiology_count['orderCode']=='BLDCUL']


import sys
sys.exit()

# Show
print microbiology_count[['BLDCUL', 'URICUL', 'WOUCUL', 'SPTCUL']]
print microbiology_count.sum()
print microbiology_count

import sys
sys.exit()
"""
"""
# Plot
microbiology_count.plot(kind='pie')

full = microbiology.groupby(by=['orderCode', 'organismCode', 'antibioticCode']).size() 
full = full.sort_values(ascending=False)

print full

full = full.reset_index()
full.to_csv('temporal.csv')
"""


"""
data = pd.read_csv('temporal.csv')
data = data[data['orderCode'].isin(['URICUL', 'WOUCUL', 'BLDCUL', 'SPTCUL'])]


for i,g in data.groupby('orderCode'):
  g = g[g['0']>1000]
  g = g[['organismCode', 'antibioticCode', '0']]
  g = g.set_index(['organismCode', 'antibioticCode'])
  g = g.unstack()
  print g

  plt.figure()
  sns.heatmap(g, linewidths=.5, square=True, vmin=np.nanmin(g), vmax=np.nanmax(g))
  plt.title(i)

  g = g.fillna(0)

  sns.clustermap(g, center=0, cmap="vlag", linewidths=.75, figsize=(5,5))
  plt.title(i)
"""

#species = ['streptococcus', 'escherichia', 'staphylococcus']

cul = 'urine'

# Load organisms
abxs = pd.read_csv('antibiotics.csv')
orgs = pd.read_csv('organisms.csv')
data = pd.read_csv('resistance-%s.csv' % cul)
freq = pd.read_csv('frequency-tests-%s.csv' % cul)

# Keep interesting columns
orgs = orgs[['organismCode', 'specieName']]
freq = freq[['organismCode', 'antibioticCode', 'freq']]
abxs = abxs[['antibioticCode', 'antibioticClass']]

# Drop duplicates
orgs = orgs.drop_duplicates()
data = data.drop_duplicates()
freq = freq.drop_duplicates()

# Merge
data = data.merge(abxs, on='antibioticCode', how='inner')
data = data.merge(orgs, on='organismCode', how='inner')
data = data.merge(freq, on=['organismCode', 'antibioticCode'], how='inner')
#data = data[data['sari']<1.0]

# Remove duplicates
data = data.drop_duplicates()
data = data[~data['organismCode'].isin(['A_ISOLATED', 'A_ANAEROBE',
  'A_MANAEROBE', 'A_SFLORA', 'A_NYI'])]
#data = data[~data['antibioticCode'].isin(['AESBL', 'AMLS'])]

data.to_csv('./antibiogram_data_sample.csv')

data.loc[pd.isnull(data['specieName']), 'specieName'] = '_na'
data.loc[pd.isnull(data['antibioticClass']), 'antibioticClass'] = '_na'
data = data.dropna(how='any', axis=0)
data = data[data['freq']>50]
data = data[['organismCode', 'antibioticCode', 'antibioticClass', 'specieName', 'sari']]




# Create data
data = data.set_index(['organismCode', 
                       'antibioticCode', 
                       'specieName',
                       'antibioticClass'])

data = data.unstack(['antibioticCode', 'antibioticClass'])
data[data==1] = np.nan
mask = pd.isnull(data)
data = data.fillna(0.00001)


def _get_colors(index, column, palette):
  # Get species
  species = index.get_level_values(column).unique().sort_values()
  netwpal = ['gray'] + sns.husl_palette(len(species), s=.45)
  #netwpal = ['gray'] + list(sns.color_palette('Set2', len(species)+1, .75))
  #netwpal = ['gray'] + list(sns.color_palette(palette, len(species)+1, .45))
  netwmap = dict(zip(map(str, species), netwpal))
  # Convert the palette to vectors that will be drawn on the side of the matrix
  networks = index.get_level_values(column)
  network_colors = pd.Series(networks, index=index).map(netwmap)
  return species, netwpal, network_colors

# Get species
vals1, pal1, col1 = _get_colors(data.index, 'specieName', 'nipy_spectral')
vals2, pal2, col2 = _get_colors(data.columns, 'antibioticClass', 'tab20b')


# Show palette
#sns.palplot(pal1)
#print vals1

#sns.palplot(pal2)


#plt.show()

methods = ['single', 'complete', 'average', 'weighted', 'centroid', 'ward']
metrics = ['euclidean', 'cityblock', 'cosine', 'hamming', 'jaccard', 'chebyshev', 
'canberra', 'braycurtis']

methods = ['ward', 'average', 'weighted', 'centroid']
metrics = ['euclidean', 'braycurtis', 'chebyshev']

methods = ['weighted', 'ward']
metrics = ['braycurtis', 'correlation']

#methods = ['ward']
#metrics = ['euclidean']

for method in methods:
  for metric in metrics:

    try :
      # Reds, RdYlGn_r
      grid = sns.clustermap(data, center=0.5, method=method, metric=metric, 
        vmin=np.nanmin(data), vmax=np.nanmax(data), mask=mask,
        cmap=sns.color_palette("Reds", desat=0.5, n_colors=10), 
        linewidths=.75, figsize=(5,5), xticklabels=True, yticklabels=True,
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
      print(metric, method, 'success')
    except:
      print(metric, method, 'failed')

plt.show()
