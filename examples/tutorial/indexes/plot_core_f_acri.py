"""
Collateral Sensitivity Index (``ACSI``)
=======================================

The Collateral Sensitivity Index - ``ACSI`` ...

.. warning:: Pending...!
"""


#%%
# First, lets create the susceptibility test records dataset

# Libraries
import pandas as pd

from pyamr.datasets.load import fixture

# ----------------------------------
# Create data
# ----------------------------------
# Load the fixture_05.csv file.
susceptibility = fixture(name='fixture_06.csv')

# Format DataFrame
susceptibility.SENSITIVITY = \
    susceptibility.SENSITIVITY.replace({
        'resistant': 'R',
        'intermediate': 'I',
        'sensitive': 'S'
})

#%%
# Lets see the susceptibility test records
susceptibility.head(10)



#%%
# Lets compute the Antimicrobial Collateral Sensitivity Index or ``ACSI``

# ------------------------------------------
# Compute the index
# ------------------------------------------
# Libraries
from pyamr.core.acsi import ACSI

# Compute index
contingency, combinations = \
    ACSI().compute(susceptibility,
        groupby=[
            'DATE',
            'SPECIMEN',
            'MICROORGANISM'
        ],
        return_combinations=True)

# Show
print("\nCombinations:")
print(combinations)
print("\nContingency:")
print(contingency)

#%%
# Lets see the contingency matrix

# Rename for docs display
rename = {
    'MICROORGANISM': 'ORGANISM',
    'ANTIMICROBIAL_x': 'ANTIBIOTIC_x',
    'ANTIMICROBIAL_y': 'ANTIBIOTIC_y'
}

# Show
contingency \
    .reset_index() \
    .rename(columns=rename) \
    .round(decimals=3)


#%%
#
# Lets compute and visualise the ``overall`` contingency matrix

# Lets compute the overall index
contingency = ACSI().compute(
    combinations.reset_index(),
    groupby=[],
    flag_combinations=True,
    return_combinations=False
)

# Show
print(contingency)

# Display
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Create index with all pairs
index = pd.MultiIndex.from_product(
    [susceptibility.ANTIMICROBIAL.unique(),
     susceptibility.ANTIMICROBIAL.unique()]
)

# Reformat
aux = contingency['acsi'] \
    .reindex(index, fill_value=np.nan)\
    .unstack()

# Display
sns.heatmap(data=aux * 100, annot=True, linewidth=.5,
            cmap='coolwarm', vmin=-70, vmax=70, center=0,
            square=True)

# Show
plt.show()

#%%
# Lets compute and visualise the ``temporal`` contingency matrix

# Lets compute the overall index
contingency = ACSI().compute(
    combinations.reset_index(),
    groupby=['DATE'],
    flag_combinations=True,
    return_combinations=False)

# Show
print(contingency)

# .. note:: Look for a nice visualisation of a matrix over time. In
#           addition to python libraries such as plotly, animations,
#           ... we can also check for js libraries such as Apache
#           echarts.