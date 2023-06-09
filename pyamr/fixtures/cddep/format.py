"""
Author: Bernard Hernandez
Date: 08/06/2023
Description:

    This script creates the susceptibility.csv and prescriptions.csv
    files which translate the information in summary.csv into a
    database-like format.
"""
# Libraries
import pandas as pd


def create_raw_data_from_summary_table(df):
    """Create raw susceptibility and prescription data from summary.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame with the summary data

    Returns
    -------

    """
    # Variable
    keep = ['DATE', 'MICROORGANISM', 'ANTIMICROBIAL']

    # Indexes
    idxr = df.index.repeat(df.R)
    idxs = df.index.repeat(df.S)
    idxu = df.index.repeat(df.USE)

    # Compute partial DataFrames
    r = df[keep].reindex(idxr).assign(sensitivity='resistant')
    s = df[keep].reindex(idxs).assign(sensitivity='sensitive')
    u = df[keep].reindex(idxu).assign(dose='standard')

    # Return
    return pd.concat([r, s]), u



# -----------------------------------------------
# Main
# -----------------------------------------------
# Load summary table
smmry = pd.read_csv('./summary.csv')

# Add additional columns
smmry['S'] = smmry.ISOLATES - smmry.R

# Create raw data.
susceptibility, prescription = \
    create_raw_data_from_summary_table(smmry)

# .. note:: Uncomment if you need to create a simulation of
#           the raw susceptibility and prescription data based
#           on the aggregated measurements.

# Save
#susceptibility.to_csv('./susceptibility_tmp.csv', index=False)
#prescription.to_csv('./prescriptions_tmp.csv', index=False)