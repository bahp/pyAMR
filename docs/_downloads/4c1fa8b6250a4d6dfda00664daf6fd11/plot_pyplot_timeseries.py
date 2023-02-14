"""
Plotly - Timeseries
-------------------

.. todo:: Explain and Simplify

.. todo: Frequency might not be working?
         Frequency can be computed as sum of columns.

"""

# Libraries
import sys
import glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
from pyamr.core.freq import Frequency
from pyamr.datasets.load import load_data_nhs

"""

# --------------------------------------------------------------------
#                               Main
# --------------------------------------------------------------------
# Load data
data, antibiotics, organisms = load_data_nhs()

# Count records per specimen code
specimen_code_count = data \
    .groupby('laboratory_number').head(1) \
    .specimen_code.value_counts(normalize=True) \
    .sort_values(ascending=False)

# Filter most frequent specimens
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:1])]

# -------------------------------------------
# Compute Freq and SARI
# -------------------------------------------
# Create instance
freq = Frequency(column_antibiotic='antimicrobial_code',
                 column_organism='microorganism_code',
                 column_date='date_received',
                 column_outcome='sensitivity')

# Create daily frequency
daily = freq.compute(data, strategy='ITI',
                      by_category='pairs',
                      fs='1M')

daily['freq'] = daily.sum(axis=1)

import plotly.express as px
import pandas as pd

print(daily)

daily = daily.reset_index()
daily = daily[daily.SPECIE.isin(['ECOL', 'PSEUD']) &
              daily.ANTIBIOTIC.isin(['AAUG'])]



fig = px.bar(daily, x='DATE', y='freq',
    title='Time Series with Range Slider and Selectors',
    facet_col='SPECIE')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.show()
"""