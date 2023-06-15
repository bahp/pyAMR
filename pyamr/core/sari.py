# Import libraries
import warnings
import pandas as pd


# -------------------------------------------------------------------------
#                            helper methods
# -------------------------------------------------------------------------
def _check_dataframe(dataframe):
    """Ensure the three columns are available.

    It also fills the empty values with zeros. This is valid
    for SARI because the columns just represent the number of
    records in that category. Thus, nan is equivalent to 0.
    """
    # Check there is at least one column.
    if not 'resistant' in dataframe and \
       not 'sensitive' in dataframe and \
       not 'intermediate' in dataframe:
       raise Exception("""
        To compute the SARI at least one of the following
        columns must be present in the DataFrame (resistant,
        sensitive, intermediate)""")

    # Copy
    aux = dataframe.copy(deep=True)

    # Add missing columns
    if not 'resistant' in dataframe:
        aux['resistant'] = 0
    if not 'intermediate' in  dataframe:
        aux['intermediate'] = 0
    if not 'sensitive' in dataframe:
        aux['sensitive'] = 0

    # Fill missing.
    aux.resistant.fillna(0, inplace=True)
    aux.intermediate.fillna(0, inplace=True)
    aux.sensitive.fillna(0, inplace=True)

    # return
    return aux


def sari(dataframe=None, strategy='hard', **kwargs):
    """Computes the Single Antimicrobial Resistance Index.

    Parameters
    ----------
    dataframe: pd.DataFrame
        A dataframe with the susceptibility test interpretations
        as columns. The default strategies used (see below) expect
        the following columns ['sensitive', 'intermediate', 'resistant']
        and if they do not appear they weill be set to zeros.

    strategy: string or func, default='hard'
        The method used to compute sari. The possible options
        are 'soft', 'medium' and 'hard'. In addition, a function
        with the following signature func(dataframe, **kwargs)
        can be passed.

            (i) ``basic`` as R / R+S
            (ii) ``soft``    as R / R+I+S
            (iii) ``medium``  as R+0.5I / R+0.5I+S
            (iv) ``hard``  as R+I / R+I+S

    **kwargs: arguments to pass the strategy function.

    Returns
    -------
    pd.Series
        The resistance index
    """
    # Ensure that exists
    aux = _check_dataframe(dataframe)

    # Extract vectors
    r = aux['resistant']
    i = aux['intermediate']
    s = aux['sensitive']

    # Call the function
    if callable(strategy):
        return strategy(aux, **kwargs)

    # Check strategy.
    if strategy not in ['soft', 'medium', 'hard', 'basic']:
        raise ValueError("""
              The strategy '{0}' is not supported. Please
              use one of the following: soft, medium, hard
              or basic""".format(strategy))

    # Compute
    if strategy == 'hard':
        return (r + i) / (r + i + s)
    elif strategy == 'medium':
        return (r + 0.5*i) / (r + i + s)
    elif strategy == 'soft':
        return r / (r + i + s)
    elif strategy == 'basic':
        return r / (r + s)


class SARI:
    """Single Antimicrobial Resistance Index.
    """
    # Attributes
    c_spe = 'SPECIMEN'
    c_org = 'MICROORGANISM'
    c_abx = 'ANTIMICROBIAL'
    c_dat = 'DATE'
    c_out = 'SENSITIVITY'

    def __init__(self, groupby=[c_spe,
                                c_org,
                                c_abx,
                                c_out]):
        """Constructor.

        Parameters
        ----------
        groupby: list
            The labels of the columns to groupby.

        Returns
        --------
        SARI instance
        """
        self.groupby = groupby


    def rolling(self, dataframe, period, cdate, shift=None):
        """Computed metric using a rolling approach."""
        if shift is None:
            warnings.warn("""
                The input parameter <shift> is None. Thus, the value 
                of the input parameter <period> (%s) has been used."""
                % period)
            shift = period

        # Grouper
        grouper = [pd.Grouper(freq=shift, key=cdate)]
        grouper = grouper + self.groupby

        # Compute frequencies
        freqs = dataframe.groupby(grouper) \
            .size().unstack().reset_index() \
            .set_index(cdate).groupby(grouper[1:-1]) \
            .rolling(window=period, min_periods=1) \
            .sum().fillna(0)

        # Return
        return freqs


    def grouping(self, dataframe, period, cdate):
        """Computes metric using independent groups.
        """
        # Create grouper
        if hasattr(dataframe[cdate].dt, str(period)):
            grouper = [getattr(dataframe[cdate].dt, period)]
        else:
            grouper = [pd.Grouper(freq=period, key=cdate)]
        grouper = self.groupby + grouper

        # Compute sensitivity counts
        freqs = dataframe.groupby(grouper) \
            .size().unstack(level=-2) \
            .fillna(0)

        # Return
        return freqs


    def compute(self, dataframe, period=None, shift=None, cdate=None,
                return_frequencies=True, **kwargs):
        """Computes Single Antimicrobial Resistance Index.

        .. todo: Add parameters to rolling!
        .. todo: Place value at the left, center, right of window?
        .. todo: Ensure that works when time gaps present!
        .. todo: Compare period > shift
        .. todo: Warning if dates NaN
        .. todo: Warning if elements in groupby any all NaN!
        .. todo: Warning if not all samples tested with same antimicrobials

        Examples
        --------

        ======= ====== =======================================================
        shift   period description
        ======= ====== =======================================================
        None    None   Uses all data (agnostic to time)
        None    year   Value every year using whole year's data.
        None    2D     Value every 2 days using 2 days data.
        2D      2D     Value every 2 days using 2 days data.
        None    2      ``Invalid``
        2D      2      ``Invalid`` Value every 2 days using 2x2D=4 days data.
        2D      None   ``Invalid`` - period cannot be None (in this case)
        2D      year   ``Invalid`` - period cannot be a year (in this case)
        year    --     ``Invalid`` - shift cannot be a named time.
        2       --     ``Invalid`` - shift cannot be a number.
        ======= ====== =======================================================

        .. note:: Using shift=2D and period=2D is equivalent to shift=2D and period=1.

        Parameters
        ----------
        dataframe: pd.DataFrame
            A dataframe with the susceptibility test interpretations
            as columns. The default strategies used (see below) expect
            the following columns ['sensitive', 'intermediate', 'resistant']
            and if they do not appear they weill be set to zeros.

        shift: str
            Frequency (datetime) value to group by when applying a rolling window.

        period: str, int
            If used alone (shift=None) is the value used to create groups (e.g. year).
            The whole data within the groups will be used to compute the metrics. On
            the contrary, when used in combinations with shift, it indicates the
            interval used to compute the metrics (e.g. 2D, 2 times the shift value)

        cdate: string, default=None
            The column that will be used as date.

        return_frequencies: boolean, default=True
            Whether to return the frequencies or just the resistance index.

        strategy: string or func, default='hard'
            The method used to compute sari. The possible options
            are 'soft', 'medium' and 'hard'. In addition, a function
            with the following signature func(DataFrame, **kwargs)
            can be passed.

                (i) ``basic`` as R / R+S
                (ii) ``soft``    as R / R+I+S
                (iii) ``medium``  as R+0.5I / R+0.5I+S
                (iv) ``hard``  as R+I / R+I+S

        **kwargs: arguments to pass the strategy function.

        Returns
        -------
        pd.Series or pd.DataFrame
            The resistance index (pd.Series) or a pd.DataFrame with the
            resistance index (sari) and the frequencies.
        """
        # Copy DataFrame
        aux = dataframe.copy(deep=True)

        # Not allowing period to be a number. The main reason is that the
        # most common interpretation is that scenarios with shift=1D
        # period=2D and shift=1D period=2 should be the same. However, the
        # results are actually different. Because period=2 in rolling will
        # use two adjacent rows without considering time. This introduces
        # inconsistencies where there are time gaps without data.
        if period is not None:
            if not isinstance(period, str):
                raise ValueError("""
                    The input parameter <period> cannot be of %s. Ensure 
                    it is either None or a valid string such as 2D or year.
                    """ % type(period))

        # ------------------------------------------
        # Frequencies
        # ------------------------------------------
        # Compute frequencies
        if period is None and shift is None:
            freqs = aux.groupby(self.groupby) \
                .size().unstack().fillna(0)

        else:

            # Format as datetime
            aux[cdate] = pd.to_datetime(aux[cdate])

            if shift is None:
                freqs = self.grouping(dataframe=aux,
                                      period=period,
                                      cdate=cdate)
            else:
                freqs = self.rolling(dataframe=aux,
                                     period=period,
                                     shift=shift,
                                     cdate=cdate)

        # Remove index name.
        freqs.columns.name = None

        # -------------------
        # Sari
        # -------------------
        # Compute sari
        s = sari(freqs, **kwargs).rename('sari')

        # Return
        if return_frequencies:
            freqs['freq'] = freqs.sum(axis=1)
            freqs['sari'] = sari(freqs, **kwargs)
            return freqs
        return s











if __name__ == '__main__': # pragma: no cover

    # Libraries
    import pandas as pd
    import matplotlib as mpl

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
         return_frequencies=True)

    # Compute SARI temporal (ITI)
    sari_iti = sari.compute(data, shift='2D',
         period='2D', cdate='DATE')

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
    print("\n\n")




    # -----------------------
    # Full test
    # -----------------------
    from itertools import product

    # Define possible values
    values = [2, '2D', None, 'year']
    combos = list(product(values, values))

    # Show
    print("\n\nCombinations of params <shift> and <period>:")

    # Loop
    for i, (shift, period) in enumerate(combos):
        print("%2s/%2s. Computing... shift=%-5s | period=%-5s ==> " % \
              (i+1, len(combos), shift, period), end="")
        try:
            s = sari.compute(data,
                shift=shift, period=period, cdate='DATE')
            print("Ok!")
            #print(s)
            #print("\n\n" + "="*80)
        except Exception as e:
            print(e)






















"""
# Import libraries
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.datasets import load

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# -----------------------
# Load data
# -----------------------
# Load sample data
data = load.dataset_epicimpoc_susceptibility_year(nrows=1000000)

# Keep only relevant columns
data = data[['antibioticCode',
           'organismCode',
           'dateReceived',
           'sensitivity']]


# Filter for two examples
is_org = data['organismCode']=='ECOL'
is_abx = data['antibioticCode'].isin(['AAUG'])
data = data[is_abx & is_org]

# -------------------------
# Create frequency instance
# -------------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
               column_organism='organismCode',
               column_date='dateReceived',
               column_outcome='sensitivity')


# Compute frequencies daily
daily = freq.compute(data, strategy='ITI',
                           by_category='pairs',
                           fs='1D')

# Compute frequencies monthly
monthly = freq.compute(data, strategy='ITI',
                           by_category='pairs',
                           fs='1M')

# Compute frequencies overlapping
oti_1 = freq.compute(data, strategy='OTI',
                         by_category='pairs',
                         wshift='1D',
                         wsize=90)

# -------------------------
# Create sari instance
# -------------------------
# Create instance
sari_daily = SARI(strategy='hard').compute(daily)
sari_monthly = SARI(strategy='hard').compute(monthly)
sari_oti_1 = SARI(strategy='hard').compute(oti_1)

# -------
# Plot
# -------
# Show comparison for each pair
f, axes = plt.subplots(4, 1, figsize=(15,8))

# Flatten axes
axes = axes.flatten()

# Plot ITI (monthly)
for i,(pair, group) in enumerate(sari_daily.groupby(level=[0,1])):
    group.index = group.index.droplevel([0,1])
    group['sari'].plot(marker='o', ms=3, label=pair,
      linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
      ax=axes[0])

# Plot ITI (monthly)
for i,(pair, group) in enumerate(sari_monthly.groupby(level=[0,1])):
    group.index = group.index.droplevel([0,1])
    group['sari'].plot(marker='o', ms=3, label=pair,
      linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
      ax=axes[1])

# Plot OTI (daily with size 30)
for i,(pair, group) in enumerate(sari_oti_1.groupby(level=[0,1])):
    group.index = group.index.droplevel([0,1])
    group['sari'].plot(marker='o', ms=3, label=pair,
      linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
      ax=axes[2])

# Set legend
for ax in axes:
    ax.legend()
    ax.set_xlabel('')
    ax.grid(True)

# Set titles
axes[0].set_ylabel('Daily')
axes[1].set_ylabel('Monthly')
axes[2].set_ylabel('OTI(1D,90)')

# Show
plt.show()
"""
