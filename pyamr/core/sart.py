# Libraries
import warnings
import pandas as pd

# Own
from pyamr.core.sari import SARI

class SART:

    # Attributes
    c_spe = 'SPECIMEN'
    c_org = 'MICROORGANISM'
    c_abx = 'ANTIMICROBIAL'
    c_dat = 'DATE'
    c_out = 'SENSITIVITY'
    c_res = 'RESISTANCE'

    def __init__(self, column_specimen=c_spe,
                       column_microorganism=c_org,
                       column_antimicrobial=c_abx,
                       column_date=c_dat,
                       column_outcome=c_out,
                       column_resistance=c_res):
        """Constructor.

        Parameters
        ----------
        groupby: list
            The labels of the columns to groupby.

        Returns
        --------
        SARI instance
        """
        # Columns
        self.c_spe = column_specimen
        self.c_org = column_microorganism
        self.c_abx = column_antimicrobial
        self.c_dat = column_date
        self.c_out = column_outcome
        self.c_res = column_resistance

        # Groupby
        self.groupby = [self.c_spe,
                        self.c_org,
                        self.c_abx,
                        self.c_out]

    def compute(self, dataframe, period='180D', shift='30D', cdate=None,
                return_objects=True, **kwargs):
        """Computes single antibiotic resistance index.

        .. todo: Add parameters to rolling!
        .. todo: Place value at the left, center, right of window?
        .. todo: Ensure that works when time gaps present!
        .. todo: Carefull with various indexes!

        Parameters
        ----------
        dataframe: pd.DataFrame
            It might receive two different types of DataFrames.

            The first option is a DataFrame with the raw susceptibility test
            records where the interpretation ('sensitive', 'intermediate',
            'resistant') that will be used to compute the sari.

            The second option is a DataFrame with the sari values already
            computed.

        shift: str
            Frequency value to pass to pd.Grouper.

        period: str, int
            Window value to pass to pd.rolling.

        cdate: string, default=None
            The column that will be used as date.

        return_frequencies: boolean, default=True
            Whether to return the frequencies or just the resistance index.

        strategy: string or func, default='hard'
            The method used to compute sari. The possible options
            are 'soft', 'medium' and 'hard'. In addition, a function
            with the following signature func(DataFrame, **kwargs)
            can be passed.

                (i) ``soft``    as R / R+I+S
                (ii) ``medium`` as R / R+S
                (iii) ``hard``  as R+I / R+I+S
                (iv) ``other``  as R+0.5I / R+0.5I+S [Not yet]

        **kwargs: arguments to pass the strategy function.

        Returns
        -------
        pd.Series or pd.DataFrame
            The resistance index (pd.Series) or a pd.DataFrame with the
            resistance index (sari) and the frequencies.
        """
        # Libraries
        import numpy as np
        import pandas as pd
        import statsmodels.api as sm

        # Libraries
        from pyamr.core.sari import SARI
        from pyamr.core.regression.wls import WLSWrapper
        from pyamr.metrics.weights import SigmoidA

        # Copy DataFrame
        aux = dataframe.copy(deep=True)

        # ------------------------------
        # Compute resistance time-series
        # ------------------------------
        # Create SARI instance
        sar = SARI(groupby=self.groupby)

        # Compute sari time-series
        sari_oti = sar.compute(aux, shift=shift,
            period=period, cdate='date_received')

        sari_oti = sari_oti.reset_index()

        # ------------------------
        # Compute resistance trend
        # ------------------------
        # Group by tuples
        groups = sari_oti.groupby(self.groupby[:-1])

        # Save
        objs = []

        # Loop
        for i, (name, group) in enumerate(groups):
            print("%2s/%2s. Computing... %s" % (i+1, len(groups), str(name)))

            # Warning
            if aux.shape[0] < 2:
                warnings.warn("""
                     {}:
                     There is only one single point and therefore the
                     resistance trend cannot be estimated. To generate a more
                     granular time series please reduce the value of <shift> 
                     or alternative find a more complete dataset.\n""".format(name))
                continue

            # Interpolate (if missing dates)
            aux = group \
                .set_index('date_received') \
                .resample(shift) \
                .interpolate(method='linear')

            # Extract variables
            x = np.arange(len(aux.sari.values))
            y = aux.sari.values * 100
            f = aux.freq.values

            # Create method to compute weights from frequencies
            W = SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0)

            # Note that the function fit will call M.weights(weights) inside and will
            # store the M converter in the instance. Therefore, the code executed is
            # equivalent to <weights=M.weights(f)> with the only difference being that
            # the weight converter is not saved.
            wls = WLSWrapper(estimator=sm.WLS).fit( \
                exog=x, endog=y, trend='c', weights=f,
                W=W, missing='raise')

            # Add pearson correlation coefficient
            wls._result['pearson'] = group.sari.corr(group.freq)

            # Append object
            objs += [(name, wls)]

        # Construct DataFrame
        table = pd.DataFrame([
            obj.as_series().append(
                pd.Series({
                    self.c_spe: name[0],
                    self.c_org: name[1],
                    self.c_abx: name[2]
                })
            ) for name, obj in objs])

        # Set index information
        table = table.set_index([
            self.c_spe,
            self.c_org,
            self.c_abx])

        # Return
        if return_objects:
            return table, objs
        return table



if __name__ == '__main__': # pragma: no cover

    # Libraries
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    # Import own libraries
    from pyamr.datasets.load import load_data_nhs

    # -------------------------
    # Configuration
    # -------------------------
    # Configure seaborn style (context=talk)
    sns.set(style="white")

    # Set matplotlib
    mpl.rcParams['xtick.labelsize'] = 9
    mpl.rcParams['ytick.labelsize'] = 9
    mpl.rcParams['axes.titlesize'] = 11
    mpl.rcParams['legend.fontsize'] = 9

    # Pandas configuration
    pd.set_option('display.max_colwidth', 40)
    pd.set_option('display.width', 300)
    pd.set_option('display.precision', 4)

    # Numpy configuration
    np.set_printoptions(precision=2)

    # -------------------------------------------
    # Load data
    # -------------------------------------------
    # Load data
    data, antimicrobials, microorganisms = load_data_nhs()

    # Show
    print("\nData:")
    print(data)
    print("\nColumns:")
    print(data.columns)
    print("\nDtypes:")
    print(data.dtypes)

    # Select tuples
    spec = ['URICUL']
    orgs = ['ECOL']
    abxs = ['ACELX', 'ACIP', 'AAMPC', 'ATRI', 'AAUG',
            'AMER', 'ANIT', 'AAMI', 'ACTX', 'ATAZ',
            'AGEN', 'AERT', 'ACAZ', 'AMEC', 'ACXT']

    # Filter
    idxs_spec = data.specimen_code.isin(spec)
    idxs_orgs = data.microorganism_code.isin(orgs)
    idxs_abxs = data.antimicrobial_code.isin(abxs)

    # Filter
    data = data[idxs_spec & idxs_orgs & idxs_abxs]

    # Filter dates (2016-2018 missing)
    data = data[data.date_received.between('2008-01-01', '2016-12-31')]


    from pyamr.core.sart import SART

    # Create instance
    sar = SART(column_specimen='specimen_code',
               column_microorganism='microorganism_code',
               column_antimicrobial='antimicrobial_code',
               column_date='date_received',
               column_outcome='sensitivity',
               column_resistance='sari')

    # Compute resistance trends
    table = sar.compute(data, shift='30D', period='180D')

    print(table)

    import sys
    sys.exit()

    # -------------------------------------------
    # Compute OTI sari (temporal)
    # -------------------------------------------
    # Generic
    import statsmodels.api as sm
    import statsmodels.robust.norms as norms

    # Libraries
    from pyamr.core.sari import SARI
    from pyamr.core.sart import SART
    from pyamr.datasets.load import make_timeseries
    from pyamr.core.regression.wls import WLSWrapper
    from pyamr.metrics.weights import SigmoidA

    # Variables
    shift, period = '30D', '180D'

    # Create SARI instance
    sar = SARI(groupby=['specimen_code',
                        'microorganism_code',
                        'antimicrobial_code',
                        'sensitivity'])

    # Compute SARI overall
    sari_overall = sar.compute(data,
         return_frequencies=True)

    # Compute sari time-series
    oti = sar.compute(data, shift=shift,
         period=period, cdate='date_received')

    # Show
    print("\nSARI:")
    print(oti)


    # -------------------------------------------
    # Compute resistance trend
    # -------------------------------------------
    # .. note: Be careful that there might be intervals (e.g. months)
    #          which do not appear in the DataFrame because there was
    #          no data (freq=0) to compute the resistance (SARI).

    #sart = SART(column_specimen='specimen_code',
    #            column_microorganism='microorganism_name',
    #            column_antimicrobial='antimicrobial_name',
    #            column_outcome='sensitivity',
    #            column_resistance='sari')#



    #import sys
    #sys.exit()


    # Group by tuples
    groups = oti.reset_index()\
        .groupby(['specimen_code',
                  'microorganism_code',
                  'antimicrobial_code'])

    # Save
    objs = []

    # Loop
    for i, (name, group) in enumerate(groups):
        print("%2s/%2s. Computing... %s" % (i, len(groups), str(name)))

        # Interpolate (if missing dates)
        aux = group \
            .set_index('date_received') \
            .resample(shift) \
            .interpolate(method='linear')

        # Extract variables
        x = np.arange(len(aux.sari.values))
        y = aux.sari.values * 100
        f = aux.freq.values

        # Create method to compute weights from frequencies
        W = SigmoidA(r=200, g=0.5, offset=0.0, scale=1.0)

        # Note that the function fit will call M.weights(weights) inside and will
        # store the M converter in the instance. Therefore, the code executed is
        # equivalent to <weights=M.weights(f)> with the only difference being that
        # the weight converter is not saved.
        wls = WLSWrapper(estimator=sm.WLS).fit( \
            exog=x, endog=y, trend='c', weights=f,
            W=W, missing='raise')

        # Add pearson correlation coefficient
        wls._result['pearson'] = group.sari.corr(group.freq)

        # Display
        # This example shows how to make predictions using the wrapper and how
        # to plot the result in data. In addition, it compares the intervals
        # provided by get_prediction (confidence intervals) and the intervals
        # provided by wls_prediction_std (prediction intervals).
        #
        # To Do: Implement methods to compute CI and PI (see regression).

        # Variables.
        start, end = None, 230

        # Compute predictions (exogenous?). It returns a 2D array
        # where the rows contain the time (t), the mean, the lower
        # and upper confidence (or prediction?) interval.
        preds = wls.get_prediction(start=start, end=end)

        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(11, 5))

        # Plotting confidence intervals
        # -----------------------------
        # Plot truth values.
        ax.plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
                markeredgecolor='k', markeredgewidth=0.5,
                markersize=5, linewidth=0.75, label='Observed')

        # Plot forecasted values.
        ax.plot(preds[0, :], preds[1, :], color='#FF0000', alpha=1.00,
                linewidth=2.0, label=wls._identifier(short=True))

        # Plot the confidence intervals.
        ax.fill_between(preds[0, :], preds[2, :],
                        preds[3, :],
                        color='r',
                        alpha=0.1)

        # Legend
        plt.legend()
        plt.title(name)

        # Append object
        objs += [(name, wls)]




    # -------------------------------------------
    # Plotting Table Graph
    # -------------------------------------------
    # Libraries
    from pyamr.graphics.table_graph import _DEFAULT_CONFIGURATION
    from pyamr.graphics.table_graph import vlinebgplot

    # Configuration
    info = _DEFAULT_CONFIGURATION

    rename = {
        'wls-x1_coef': 'sart_m',
        #'wls-const_coef': 'offset',
        'wls-rsquared': 'r2',
        'wls-rsquared_adj': 'r2_adj',
        'wls-m_skew': 'skew',
        'wls-m_kurtosis': 'kurtosis',
        'wls-m_jb_prob': 'jb',
        'wls-m_dw': 'dw',
        'wls-const_tprob': 'ptm',
        'wls-x1_tprob': 'ptn',
        'wls-pearson': 'pearson',
        'freq': 'freq',
    }

    # Construct DataFrame
    table = pd.DataFrame([
        obj.as_series().append(
            pd.Series({
                'specimen_code': name[0],
                'microorganism_code': name[1],
                'antimicrobial_code': name[2]
            })
        ) for name, obj in objs])

    # Set index information
    table = table.set_index([
        'specimen_code',
        'microorganism_code',
        'antimicrobial_code'
    ])

    # Combine and format
    comb = table.join(sari_overall)
    comb.index = comb.index.map('_'.join)
    comb = comb.reset_index()
    comb = comb.rename(columns=rename)
    comb['sart_y'] = comb.sart_m * 12   # Yearly trend
    comb['sari_pct'] = comb.sari * 100  # SARI percent

    # Sort by trend
    comb = comb.sort_values(by='sart_y', ascending=False)

    # Select only numeric columns
    #data = comb.select_dtypes(include=np.number)
    data = comb[[
        'index',
        'sart_m',
        'sart_y',
        'sari_pct',
        'r2',
        'r2_adj',
        'skew',
        'kurtosis',
        'jb',
        'dw',
        'ptm',
        'ptn',
        'pearson',
        'freq'
    ]]

    # Show DataFrame
    print("\nResults:")
    print(data)

    # Create pair grid
    g = sns.PairGrid(data, x_vars=data.columns[1:],
        y_vars=["index"], height=3, aspect=.45)

    # Draw a dot plot using the stripplot function
    #g.map(sns.stripplot, size=10, orient="h", jitter=False,
    #      palette="flare_r", linewidth=1, edgecolor="w")

    # Set common features
    g.set(xlabel='', ylabel='')

    # Plot strips and format axes (skipping index)
    for ax, c in zip(g.axes.flat, data.columns[1:]):

        # Get information
        d = info[c] if c in info else {}

        # Display
        # sns.stripplot(data=data, x=title, y='abx', size=10,
        #    orient="h", jitter=False, linewidth=0.75, ax=ax,
        #    edgecolor="gray", palette=d.get('cmap', None))
        #    color='b')

        # .. note: We need to use scatter plot if we want to
        #          assign colors to the markers according to
        #          their value.

        # Using scatter plot
        sns.scatterplot(data=data, x=c,  y='index', s=100,
                        ax=ax, linewidth=0.75, edgecolor='gray',
                        c=data[c], cmap=d.get('cmap', None),
                        norm=d.get('norm', None))

        # Plot vertical lines
        for e in d.get('vline', []):
            vlinebgplot(ax, top=data.shape[0], **e)

        # Configure axes
        ax.set(title=d.get('title', c),
               xlim=d.get('xlim', None),
               xticks=d.get('xticks', []),
               xlabel='', ylabel='')
        ax.tick_params(axis='y', which='both', length=0)
        ax.xaxis.grid(False)
        ax.yaxis.grid(visible=True, which='major',
                      color='gray', linestyle='-', linewidth=0.35)

    # Despine
    sns.despine(left=True, bottom=True)

    # Adjust layout
    plt.tight_layout()
    plt.show()
