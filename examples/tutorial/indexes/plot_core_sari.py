"""
Single Resistance Index (SARI)
==============================

The Single Antimicrobial Resistance Index - ``SARI`` - describes the proportion
of resistant isolates for a given set of susceptibility tests. It provides a
value within the range [0, 1] where values close to one indicate high resistance.
It is agnostic to pathogen, antibiotic and/or time. The variables ``R``, ``I`` and
``S`` represent the number of susceptibility tests with Resistant, Intermediate and
Susceptible outcomes respectively. The definition might vary slightly since the
intermediate category is not always considered.

The parameter strategy accepts three different options:

    - ``soft``   as R / (R+I+S)
    - ``medium`` as R / (R+S)
    - ``hard``   as (R+I) / (R+I+S)
    - ``other``  as (R+0.5I) / (R+0.5I+S)

..
    - ``soft``   as :math:`R / (R + I + S)`
    - ``medium`` as :math:`R / (R + S)`
    - ``hard``   as :math:`(R + I) / (R + I + S)`
    - ``other``  as :math:`(R + 0.5I) / (R + 0.5I + S)`

For more information see: :py:mod:`pyamr.core.sari.SARI`


"""

# Libraries
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Specific
from pyamr.core.sari import SARI

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# ----------------------------------
# Create data
# ----------------------------------
# Define susceptibility test records
data = [
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-04', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],

    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-04', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],

    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],

    ['2021-01-12', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-12', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
    ['2021-01-13', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-13', 'URICUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-14', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-14', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-15', 'URICUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-15', 'URICUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-16', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
    ['2021-01-16', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
]

data = pd.DataFrame(data,
    columns=['DATE',
             'SPECIMEN',
             'MICROORGANISM',
             'ANTIMICROBIAL',
             'SENSITIVITY'])


# Create SARI instance
sari = SARI(groupby=['SPECIMEN',
                     'MICROORGANISM',
                     'ANTIMICROBIAL',
                     'SENSITIVITY'])

# Compute SARI overall
sari_overall = sari.compute(data,
    return_frequencies=False)

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
# Let's display the overall resistance.
#
sari_overall.to_frame()

#%%
# Let's display the resistance time-series using **independent** time intervals (ITI)
#
sari_iti


#%%
# Let's display the resistance time-series using **overlapping** time intervals (OTI)
#
sari_oti

#%%
# .. note:: On a side note, the variable *sari_overall* returned is a ``pd.Series``.
#           However, it has been converted to a ``pd.DataFrame`` for display purposes.
#           The ``sphinx`` library used to create the documentation uses the method
#           ``_repr_html_`` from the latter to display it nicely in the docs.
