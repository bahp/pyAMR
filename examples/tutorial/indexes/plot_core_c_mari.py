"""
Multiple Resistance (``MARI``)
==============================

.. warning::
        - What visualisation could we use?
        - Create further examples with temporal visualization.
        - Add parameters to choose antimicrobials that are consistent in time and
          have enough number of isolates to give an accurate measurement.

Determination of the Multiple Antimicrobial Resistance Index or ``MARI`` follows the procedure
described by (5), in which the number of antimicrobials an isolate is resistant to (*R*) is divided by the
total number of the antimicrobials used in the study (*T*). Thus, the calculating formula for a single
isolate is shown below and it provides a value within the range [0,1] where values close to one indicate
high multi-drug resistance.

.. math::

    MARI_{ISO} = R / T

In more general scenarios, the antimicrobials to which the pathogens are tested vary among health care
centres and time, and therefore the comparison and analysis of ``MARI`` evolution in time is not straight
forward. At the moment, for simplicity, it is recommended to check that the antimicrobials selected are
available in the whole study period before applying the index.

.. note:: Please, ensure that all isolates contains records for all antimicrobials.

For more information see: :py:mod:`pyamr.core.mari.MARI`


For the sample data created below, the overall ``MARI`` for each isolate is

========== ========= =============== =========== ===============
Date       SPECIMEN   MICROORGANISM  LAB_NUMBER   MARI
========== ========= =============== =========== ===============
2021-01-01 BLDCUL    ECOL            lab1        4/10 = 0.400000
2021-01-01 BLDCUL    ECOL            lab2        0.800000
2021-01-02 BLDCUL    ECOL            lab3        0.700000
2021-01-03 BLDCUL    ECOL            lab4        0.909091
========== ========= =============== =========== ===============


Similarly, the rolling window ``MARIs`` for <BLDCUL, ECOL> are ...

========== ================== ====================== ==================
Date       MARI (1D1)          MARI (1D2)            MARI Wrong!
========== ================== ====================== ==================
2021-01-01 (0.4+0.8)/2 = 0.6  (0.4+0.8)/2     = 0.60 (0.4+0.8)/2 = 0.6
2021-01-02 0.7         = 0.7  (0.4+0.8+0.7)/3 = 0.63 (0.6+0.7)/2 = 0.65
2021-01-03 0.909091    = 0.9  (0.7+0.9)/2     = 0.80 (0.7+0.9)/2 = 0.8
========== ================== ====================== ==================

"""


# Import libraries
import warnings
import pandas as pd
import matplotlib as mpl

# Import specific libraries
from pyamr.core.mari import MARI
from pyamr.datasets.load import fixture

# Filter user warning
warnings.filterwarnings("ignore", category=UserWarning)

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# ---------------------
# Create data
# ---------------------
# Load data
data = fixture(name='fixture_05.csv')


# ---------------------
# Compute MARI
# ---------------------
# Create MARI instance
mari = MARI(groupby=['SPECIMEN',
                     'MICROORGANISM',
                     'LAB_NUMBER',
                     'SENSITIVITY'])

# Compute MARI overall
mari_overall, isolates = mari.compute(data,
    return_frequencies=True,
    return_isolates=True)

# Compute MARI temporal (ITI)
mari_iti = mari.compute(data, shift='1D',
    period='1D', cdate='DATE',
    return_isolates=False)

# Compute MARI temporal (OTI)
mari_oti = mari.compute(data, shift='1D',
    period='2D', cdate='DATE',
    return_isolates=False)

# Show
print("\nIsolates:")
print(isolates)
print("\n\n\nMARI (overall):")
print(mari_overall)
print("\n\n\nMARI (iti):")
print(mari_iti)
print("\n\n\nMARI (oti):")
print(mari_oti)


#%%
# Lets see the susceptibility test records.
data.head(15)

#%%
# Let's display the ``overall_hard`` resistance.
#
mari_overall


#%%
# Let's display the resistance time-series using ``independent`` time intervals (ITI)
#
mari_iti


#%%
# Let's display the resistance time-series using ``overlapping`` time intervals (OTI)
#
mari_oti

#%%
# Let's display the information graphically