"""
HTML - Treemap (sari)
-----------------------

.. warning:: It might take some time to load.

https://plotly.com/python/plotly-express/
https://plotly.com/python/animations/
https://plotly.com/python/treemaps/

"""
# Plotly
import plotly.express as px

# Import own libraries
from pyamr.core.sari import sari
from pyamr.datasets.load import load_data_mimic


# --------------------------------------------------------------------
#                               Main
# --------------------------------------------------------------------
# Load data
data, antimicrobials, microorganisms = load_data_mimic()

# Create DataFrame
dataframe = data.groupby(['specimen_code',
                          'microorganism_code',
                          'antimicrobial_code',
                          'sensitivity']) \
                .size().unstack().fillna(0)

# Compute frequency
dataframe['freq'] = dataframe.sum(axis=1)

# Compute sari
dataframe['sari'] = sari(dataframe, strategy='hard')
dataframe['sari_medium'] = sari(dataframe, strategy='medium')
dataframe['sari_soft'] = sari(dataframe, strategy='soft')

# Reset index
dataframe = dataframe.reset_index()

# --------------------------------------------
# Add info for popup
# --------------------------------------------
dataframe = dataframe.merge(antimicrobials,
    how='left', left_on='antimicrobial_code',
    right_on='antimicrobial_code')

# Add antimicrobials information
dataframe = dataframe.merge(microorganisms,
    how='left', left_on='microorganism_code',
    right_on='microorganism_code')

# Format dataframe
dataframe = dataframe.round(decimals=3)

# Show columns
print(dataframe.columns)

# -------------------------------------------
# Plot
# -------------------------------------------
# Show
fig = px.treemap(dataframe,
    path=['specimen_code',
          'microorganism_code',
          'antimicrobial_code'],
    #hover_name=,
    hover_data=['microorganism_name',
                'name',
                'sari_medium',
                'sari_soft'],
    values='freq',
    color='sari',
    color_continuous_scale='Reds',
    title='Treemap of <Microorganisms, Antimicrobials> pairs (MIMIC)')

# Save as html (to be used anyware in docs)
fig.write_html("../../../docs/source/_static/htmls/{0}.html" \
    .format('plot_mimic_treemap'))

# Show (script)
#fig.show()

# Show (sphinx)
fig