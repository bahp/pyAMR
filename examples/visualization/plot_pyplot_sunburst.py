"""
Plotly - Sunburst (sari)
------------------------

.. warning:: Please be patient, it might take some time to load.

"""

# Plotly
import plotly.express as px

# Import own libraries
from pyamr.datasets.load import load_data_nhs


# --------------------------------------------------------------------
#                               Main
# --------------------------------------------------------------------
# Load data
data, antibiotics, organisms = load_data_nhs(nrows=1000)

# Create DataFrame
dataframe = data.groupby(['specimen_code',
                          'microorganism_code',
                          'antimicrobial_code',
                          'sensitivity']) \
                .size().unstack().fillna(0)

# Compute frequency
dataframe['freq'] = dataframe.sum(axis=1)

# Compute sari
dataframe['sari'] = dataframe.resistant / \
    (dataframe.resistant + dataframe.sensitive)

# Reset index
dataframe = dataframe.reset_index()

# -------------------------------------------
# Plot
# -------------------------------------------
# Show
fig = px.sunburst(dataframe,
    path=['specimen_code',
          'microorganism_code',
          'antimicrobial_code'],
    values='freq',
    color='sari',
    title='Sunburst of <Microorganisms, Antimicrobials> pairs')

# Show
#fig.show()
fig