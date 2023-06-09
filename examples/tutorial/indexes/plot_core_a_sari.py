"""
Single Antimicrobial Resistance (``SARI``)
==========================================

The Single Antimicrobial Resistance Index or ``SARI`` describes the proportion
of resistant isolates for a given set of susceptibility tests. It provides a
value within the range [0, 1] where values close to one indicate high resistance.
It is agnostic to pathogen, antibiotic and/or time. The variables ``R``, ``I`` and
``S`` represent the number of susceptibility tests with Resistant, Intermediate and
Susceptible outcomes respectively. The definition might vary slightly since the
intermediate category is not always considered.

For more information see: :py:mod:`pyamr.core.sari.SARI`
"""

# Libraries
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Specific
from pyamr.core.sari import SARI
from pyamr.datasets.load import fixture

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# ----------------------------------
# Methods
# ----------------------------------
def own(aux, offset):
    """Add offset to hard"""
    # Extract vectors
    r = aux.resistant
    i = aux.intermediate
    s = aux.sensitive
    # Compute
    return ((r+i) / (r+i+s)) + offset

# ----------------------------------
# Create data
# ----------------------------------
# Load data
data = fixture(name='fixture_07.csv')

# ---------------------------------
# Compute SARI
# ---------------------------------
# Create SARI instance
sari = SARI(groupby=['SPECIMEN',
                     'MICROORGANISM',
                     'ANTIMICROBIAL',
                     'SENSITIVITY'])

# Compute SARI overall (hard)
sari_overall = sari.compute(data,
    return_frequencies=False)

# Compute SARI overall (soft)
sari_overall_soft = sari.compute(data,
    return_frequencies=False,
    strategy='soft')

# Compute SARI overall (own)
sari_overall_own = sari.compute(data,
    return_frequencies=False,
    strategy=own,
    offset=5)

# Compute SARI temporal (ITI)
sari_iti = sari.compute(data, shift='1D',
    period='1D', cdate='DATE')

# Compute SARI temporal (OTI)
sari_oti = sari.compute(data, shift='1D',
    period='2D', cdate='DATE')

# Show
print("\nSARI (overall):")
print(sari_overall)
print("\nSARI (iti):")
print(sari_iti)
print("\nSARI (oti):")
print(sari_oti)

#%%
# Lets see the susceptibility test records.
data.head(15)

#%%
# Let's display the ``overall_hard`` resistance.
#
sari_overall.to_frame()

#%%
# Let's compare with the ``overall_soft`` resistance.
#
sari_overall_soft.to_frame()

#%%
# Let's compare with the ``overall_own`` resistance.
#
sari_overall_own.to_frame()

#%%
# Let's display the resistance time-series using ``independent`` time intervals (ITI)
#
sari_iti


#%%
# Let's display the resistance time-series using ``overlapping`` time intervals (OTI)
#
sari_oti

#%%
# .. note:: On a side note, the variable *sari_overall* returned is a ``pd.Series``.
#           However, it has been converted to a ``pd.DataFrame`` for display purposes.
#           The ``sphinx`` library used to create the documentation uses the method
#           ``_repr_html_`` from the latter to display it nicely in the docs.

#%%
# Let's display the information graphically