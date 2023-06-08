"""
``DRI`` - Example using ``MIMIC``
---------------------------------

In the field of healthcare, analyzing drug resistance in antimicrobial
use is crucial for understanding and combating the growing problem of
antibiotic resistance. One example is the Drug Resistance Index o ``DRI``.
In this example, we compute such index using ``MIMIC``, comprehensive,
a widely-used and freely available healthcare database that contains
de-identified electronic health records of over 60,000 intensive care unit
patients. Within ``MIMIC``, researchers have access to rich information,
including patient demographics, clinical notes, laboratory results, and
medication records. This dataset provides the necessary data, susceptibility
and prescription information, to compute the drug resistance  index.

.. note:: In ``MIMIC``, the deidentification process for structured data
          required the removal of dates. In particular, dates were shifted
          into the future by a random offset for each individual patient in
          a consistent manner to preserve intervals, resulting in stays which
          occur sometime between the years 2100 and 2200. Time of day, day of
          the week, and approximate seasonality were conserved during date
          shifting.

"""

# Define sphinx gallery configuration
# sphinx_gallery_thumbnail_number = 2

# Libraries
import sys
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl

from pathlib import Path

try:
    __file__
    TERMINAL = True
except:
    TERMINAL = False

# -------------------------
# Configuration
# -------------------------
# Params
rc = {
    'axes.linewidth': 0.5,
    'axes.labelsize': 9,
    'axes.titlesize': 11,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
}

# Configure seaborn style (context=talk)
sns.set_theme(style="white", rc=rc)

# Configure warnings
warnings.filterwarnings("ignore",
    category=pd.errors.DtypeWarning)

# -------------------------------------------------------
# Constants
# -------------------------------------------------------
# Rename columns for susceptibility
rename_susceptibility = {
    'chartdate': 'DATE',
    'micro_specimen_id': 'LAB_NUMBER',
    'spec_type_desc': 'SPECIMEN',
    'org_name': 'MICROORGANISM',
    'ab_name': 'ANTIMICROBIAL',
    'interpretation': 'SENSITIVITY'
}

# Rename columns for prescriptions
rename_prescriptions = {
    'drug': 'DRUG'
}



#%%
# First, we need to load the ``susceptibility`` test data

# -----------------------------
# Load susceptibility test data
# -----------------------------
# Helper
subset = rename_susceptibility.values()

# Load data
path = Path('../../pyamr/datasets/mimic')
data1 = pd.read_csv(path / 'susceptibility.csv')

# Rename columns
data1 = data1.rename(columns=rename_susceptibility)

# Format data
data1 = data1[subset]
data1 = data1.dropna(subset=subset, how='any')
data1.DATE = pd.to_datetime(data1.DATE)
data1.SENSITIVITY = data1.SENSITIVITY.replace({
    'S': 'sensitive',
    'R': 'resistant',
    'I': 'intermediate',
    'P': 'pass'
})

#%%
data1.head(5)


#%%
# Lets also load the ``prescriptions`` (could be also overall usage) data

# ----------------------------
# Load prescriptions
# ----------------------------
# Load prescription data (limited to first nrows).
data2 = pd.read_csv(path / 'prescriptions.csv', nrows=100000)
data2 = data2.rename(columns=rename_prescriptions)

# Format data
data2.DRUG = data2.DRUG.str.upper()
data2['DATE'] = pd.to_datetime(data2.starttime)
data2 = data2.dropna(subset=['DATE'], how='any')

# .. note:: We are only keeping those DRUGS which have
#           the exact name of the antimicrobial tested
#           in the susceptibility test record. There are
#           also brand names that could/should be
#           included

# Filter
data2 = data2[data2.DRUG.isin(data1.ANTIMICROBIAL.unique())]

#%%
print(data2)

#%%
# Lets rename the variables.

# Rename variables
susceptibility, prescriptions = data1, data2

# Show
if TERMINAL:
    print("\nSusceptibility:")
    print(susceptibility.head(10))
    print("\nPrescriptions:")
    print(prescriptions.head(10))


#%%
# Now we need to create a summary table including the resistance
# value, which will be computed using ``SARI`` and the usage which
# will be computed manually. This summary table is required as a
# preliminary step to compute the ``DRI``.

# ------------------------
# Compute summary table
# ------------------------
# Libraries
from pyamr.core.sari import SARI

# Create sari instance
sari = SARI(groupby=[
    susceptibility.DATE.dt.year,
    #'SPECIMEN',
    'MICROORGANISM',
    'ANTIMICROBIAL',
    'SENSITIVITY']
)

# Compute susceptibility summary table
smmry1 = sari.compute(susceptibility,
    return_frequencies=True)

# .. note:: We are counting the number of rows as an indicator
#           of prescriptions. However, it would be possible to
#           sum the doses (with caution due to units, ...)

# Compute prescriptions summary table.
smmry2 = prescriptions \
    .groupby(by=[prescriptions.DATE.dt.year, 'DRUG']) \
    .DRUG.count().rename('use')
    #.DOSE.sum().rename('use')
smmry2.index.names = ['DATE', 'ANTIMICROBIAL']

# Combine both summary tables
smmry = smmry1.reset_index().merge(
    smmry2.reset_index(), how='inner',
    left_on=['DATE', 'ANTIMICROBIAL'],
    right_on=['DATE', 'ANTIMICROBIAL']
)

# Show
if TERMINAL:
    print("\nSummary:")
    print(smmry)

#%%
#
smmry


#%%
# Lets compute the ``DRI``

# -------------------------
# Compute DRI
# -------------------------
# Libraries
from pyamr.core.dri import DRI

# Instance
obj = DRI(
    column_resistance='sari',
    column_usage='use'
)

# Compute overall DRI
dri1 = obj.compute(smmry,
    groupby=['DATE'],
    return_usage=True)

# Compute DRI by organism
dri2 = obj.compute(smmry,
    groupby=['DATE', 'MICROORGANISM'],
    return_usage=True)


if TERMINAL:
    print("DRI overall:")
    print(dri1)
    print("DRI by microorganism:")
    print(dri2)

#%%
#
dri1

#%%
#
dri2

#%%
# Lets visualise the overall ``DRI``.

# --------------------------------------------
# Plot
# --------------------------------------------
# Libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Display using relplot
g = sns.relplot(data=dri1.reset_index(), x='DATE', y='dri',
    height=2, aspect=3.0, kind='line',
    linewidth=2, markersize=0, marker='o'
)

plt.tight_layout()

#%%
# Lets visualise the microorganism-wise ``DRI``.

# --------------------------------------------
# Format
# --------------------------------------------
# Copy results
aux = dri2.copy(deep=True)

# Combine with summary
aux = aux.merge(smmry, how='left',
    left_on=['DATE', 'MICROORGANISM'],
    right_on=['DATE', 'MICROORGANISM'])

# Find microorganisms with more samples
top = aux.groupby(by='MICROORGANISM') \
    .freq.sum().sort_values(ascending=False) \
    .head(5)

# Filter by top microorganisms
aux = aux[aux.MICROORGANISM.isin(top.index)]

# --------------------------------------------
# Plot
# --------------------------------------------
# Display
g = sns.relplot(data=aux,
    x='DATE', y='dri', hue='MICROORGANISM',
    row='MICROORGANISM', palette='rocket',
    #style='event', col='region', palette='palette',
    height=1.5, aspect=4.0, kind='line', legend=False,
    linewidth=2, markersize=0, marker='o')

"""
# Iterate over each subplot to customize further
for title, ax in g.axes_dict.items():
    ax.text(1., .85, title, transform=ax.transAxes,
        fontsize=9, fontweight="normal",
        horizontalalignment='right')
"""
# Configure
g.tight_layout()
g.set_titles("{row_name}")
#g.set_titles("")

# Show
plt.show()

#%%
# The top microorganisms are:
top

#%%
# The results look as follows:
aux.rename(columns={
    'intermediate': 'I',
    'sensitive': 'S',
    'resistant': 'R',
    'pass': 'P'
}).round(decimals=2)
