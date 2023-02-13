"""
Multiple Resistance (MARI)
========================================

.. warning::
        - Improve visualization.
        - Create further examples with temporal visualization.
        - Add parameters to choose antimicrobials that are consistent in time and
          have enough number of isolates to give an accurate measurement.

Determination of the Multiple Antimicrobial Resistance Index, denoted as ``MARI``,  follows the procedure
described by (5), in which the number of antimicrobials an isolate is resistant to (R) is divided by the
total number of the antimicrobials used in the study (T). Thus, the calculating formula for a single
isolate is shown below and it provides a value within the range [0,1] where values close to one indicate
high multi-drug resistance.

                                  MARI_{ISO} = R / T

In more general scenarios, the antimicrobials to which the pathogens are tested vary among health care
centres and time, and therefore the comparison and analysis of `MARI`` evolution in time is not straight
forward. At the moment, for simplicity, it is recommended to check that the antimicrobials selected are
available in the whole study period before applying the index.

For more information see: :py:mod:`pyamr.core.asai.MARI`


For the example below, the static MARI for each isolate is ...

========== ====== ==== ==== ========
Date                        MARI
========== ====== ==== ==== ========
2021-01-01 BLDCUL ECOL lab1 0.400000
2021-01-01 BLDCUL ECOL lab2 0.800000
2021-01-02 BLDCUL ECOL lab3 0.700000
2021-01-03 BLDCUL ECOL lab4 0.909091
========== ====== ==== ==== ========


The rolling window MARIs for <BLDCUL, ECOL> are ...

========== ================== ====================== ==================
Date       MARI (1D1)          MARI (1D2)            MARI Wrong!
========== ================== ====================== ==================
2021-01-01 (0.4+0.8)/2 = 0.6  (0.4+0.8)/2     = 0.60 (0.4+0.8)/2 = 0.6
2021-01-02 0.7         = 0.7  (0.4+0.8+0.7)/3 = 0.63 (0.6+0.7)/2 = 0.65
2021-01-03 0.909091    = 0.9  (0.7+0.9)/2     = 0.80 (0.7+0.9)/2 = 0.8
========== ================== ====================== ==================

"""


# Import libraries
import pandas as pd
import matplotlib as mpl

# Import specific libraries
from pyamr.core.mari import MARI

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# ---------------------
# Create data
# ---------------------
# Create data
data = [
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'ATAZ', 'sensitive'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'ACAZ', 'sensitive'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'ACXM', 'sensitive'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'AGEN', 'sensitive'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'AMER', 'resistant'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'AAMI', 'sensitive'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'ATEM', 'resistant'],
    ['2021-01-01', 'lab1', 'BLDCUL', 'ECOL', 'ACTX', 'resistant'],

    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'ATAZ', 'intermediate'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'ACAZ', 'intermediate'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'ACIP', 'intermediate'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'ACXM', 'intermediate'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'AGEN', 'resistant'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'AMER', 'resistant'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'AAMI', 'resistant'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'ATEM', 'resistant'],
    ['2021-01-01', 'lab2', 'BLDCUL', 'ECOL', 'ACTX', 'sensitive'],

    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'ATAZ', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'ACAZ', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'ACXM', 'sensitive'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'AGEN', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'AMER', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'AAMI', 'sensitive'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'ATEM', 'resistant'],
    ['2021-01-02', 'lab3', 'BLDCUL', 'ECOL', 'ACTX', 'sensitive'],

    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ATAZ', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ACAZ', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ACXM', 'sensitive'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'AGEN', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'AMER', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'AAMI', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ATEM', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ACTX', 'resistant'],
    ['2021-01-03', 'lab4', 'BLDCUL', 'ECOL', 'ANEW', 'resistant'],

    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'AAUG', 'resistant'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'ATAZ', 'resistant'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'ACAZ', 'resistant'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'ACIP', 'resistant'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'ACXM', 'sensitive'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'AGEN', 'intermediate'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'AMER', 'sensitive'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'AAMI', 'sensitive'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'ATEM', 'resistant'],
    ['2021-01-01', 'lab5', 'BLDCUL', 'CNS', 'ACTX', 'resistant'],

    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'AAUG', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'ATAZ', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'ACAZ', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'ACIP', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'ACXM', 'sensitive'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'AGEN', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'AMER', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'AAMI', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'ATEM', 'resistant'],
    ['2021-02-01', 'lab6', 'BLDCUL', 'CNS', 'ACTX', 'resistant'],

    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'ATAZ', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'ACAZ', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'ACXM', 'sensitive'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'AGEN', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'AMER', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'AAMI', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'ATEM', 'resistant'],
    ['2021-02-01', 'lab7', 'URICUL', 'ECOL', 'ACTX', 'resistant'],

    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'ATAZ', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'ACAZ', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'ACXM', 'sensitive'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'AGEN', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'AMER', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'AAMI', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'ATEM', 'resistant'],
    ['2021-02-04', 'lab8', 'URICUL', 'ECOL', 'ACTX', 'resistant'],
]



data = pd.DataFrame(data,
    columns=['DATE',
             'LAB_NUMBER',
             'SPECIMEN',
             'MICROORGANISM',
             'ANTIMICROBIAL',
             'SENSITIVITY'])

# Create SARI instance
mari = MARI(groupby=['SPECIMEN',
                     'MICROORGANISM',
                     'LAB_NUMBER',
                     'SENSITIVITY'])

# Compute SARI overall
mari_overall, isolates = mari.compute(data,
    return_frequencies=True,
    return_isolates=True)

# Compute SARI temporal (ITI)
mari_iti = mari.compute(data, shift='1D',
    period=1, cdate='DATE',
    return_isolates=False)

# Compute SARI temporal (OTI)
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
