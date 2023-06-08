"""
``ACSI`` - Example using ``MIMIC``
----------------------------------

"""

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


# Configure seaborn style (context=talk)
sns.set_theme(style="white")

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

#%%
# Let's load the ``susceptibility`` test data


# -----------------------------
# Load susceptibility test data
# -----------------------------
nrows=1000

# Helper
subset = rename_susceptibility.values()

# Load data
path = Path('../../pyamr/datasets/mimic')
data1 = pd.read_csv(path / 'susceptibility.csv', nrows=nrows)

# Rename columns
data1 = data1.rename(columns=rename_susceptibility)

# Format data
data1 = data1[subset]
data1 = data1.dropna(subset=subset, how='any')
data1.DATE = pd.to_datetime(data1.DATE)

#%%
data1.head(5)

#%%
# Let's compute the ``ACSI`` and return the combinations.
#
# .. note:: This step is quite computationally expensive since it has to create all
#           possible antimicrobial combinations within each isolate in the
#           susceptibility test data. Thus, it is recommended to save the results
#           for future analysis and/or visualisation.


# Libraries
from pyamr.core.acsi import ACSI

# Compute index
contingency, combinations = \
    ACSI().compute(data1,
    groupby=[
        'DATE',
        'SPECIMEN',
        'MICROORGANISM'
    ],
    return_combinations=True)

# Save
#contingency.to_csv('contingency_%s.csv' % nrows)
#combinations.to_csv('combinations_%s.csv' % nrows)

# Display
print("\nCombinations:")
print(combinations)
print("\nContingency:")
print(contingency)





#%%
# Let's compute the ``ACSI``.
#
# .. note:: We are loading previously computed combinations.

# Libraries
from pyamr.datasets.load import fixture

# Path
combinations = fixture(name='mimic/asci/combinations.csv')

# Lets compute the overall index
contingency = ACSI().compute(
    combinations.reset_index(),
    groupby=[],
    flag_combinations=True,
    return_combinations=False
)


#%%
# Let's visualise the result

# ------------------------------------------
# Display
# ------------------------------------------
# Display
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Get unique antimicrobials
s1 = set(combinations.ANTIMICROBIAL_x.unique())
s2 = set(combinations.ANTIMICROBIAL_x.unique())
abxs = s1.union(s2)

# Create index with all pairs
index = pd.MultiIndex.from_product([abxs, abxs])

# Reformat
aux = contingency['acsi'] \
    .reindex(index, fill_value=np.nan) \
    .unstack()

# Create figure
fig, axs = plt.subplots(nrows=1, ncols=1,
     sharey=False, sharex=False, figsize=(12, 9)
)

# Display
sns.heatmap(data=aux * 100, ax=axs,
    annot=True, annot_kws={'size':7}, square=True,
    linewidth=.5, xticklabels=True, yticklabels=True,
    cmap='coolwarm', vmin=-70, vmax=70, center=0,
    cbar_kws={'label': 'Collateral Sensitivity Index'})

# Show
plt.tight_layout()
plt.show()
