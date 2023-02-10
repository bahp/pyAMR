################################################################################
# Author:
# Date:
# Description:
#
#
#
# Copyright:
#
#
################################################################################
# Import libraries
import pandas as pd

# Import sari
from pyamr.core.sari import sari


# -------------------------------------------------------------------------
#                            helper methods
# -------------------------------------------------------------------------
class MARI:
    # Attributes
    c_lab = 'LAB_NUMBER'
    c_spe = 'SPECIMEN'
    c_org = 'MICROORGANISM'
    c_dat = 'DATE'
    c_out = 'SENSITIVITY'

    def __init__(self, groupby=[c_spe,
                                c_org,
                                c_lab,
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

    def compute(self, dataframe, shift=None, period=None, cdate=None,
                return_frequencies=True, return_isolates=True, **kwargs):
        """Computes single antibiotic resistance index.

        .. todo: Add parameters to rolling!
        .. todo: Place value at the left, center, right of window?
        .. todo: Ensure that works when time gaps present!
        .. todo: Carefull with various indexes!

        Parameters
        ----------
        dataframe: pd.DataFrame
            A dataframe with the susceptibility test interpretations
            as columns. The default strategies used (see below) expect
            the following columns ['sensitive', 'intermediate', 'resistant']
            and if they do not appear they weill be set to zeros.

        shift: str
            Frequency value to pass to pd.Grouper.

        period: str, int
            Window value to pass to pd.rolling.

        cdate: string, default=None
            The column that will be used as date.

        return_frequencies: boolean, default=True
            Whether to return the frequencies (isolates) or just the resistance index.

        return_isolates: boolean, default=True
            Whether to return the resistance index for each individual isolate.

        strategy: string or func, default='hard'
            The method used to compute sari. The possible options
            are 'soft', 'medium' and 'hard'. In addition, a function
            with the following signature func(dataframe, **kwargs)
            can be passed.

                (i) ``soft``   as R / R+I+S
                (ii) ``medium`` as R / R+S
                (iii) ``hard``  as R+I / R+I+S
                (iv) ``other``  as R+0.5I / R+0.5I+S [Not yet]

        **kwargs: arguments to pass the strategy function.

        Returns
        -------
        dataframe: pd.Series or pd.DataFrame
            The resistance index (pd.Series) or a pd.Dataframe with the
            resistance index (sari), the sums and the frequencies.

        isolates: pd.DataFrame
            The resistance index and each of the sensitivity value
            counts for each individual isolate.
        """

        # Copy DataFrame
        aux = dataframe.copy(deep=True)

        # Warning if dates NaN
        # Warning if elements in groupby any all NaN!

        # Create grouper
        grouper = []
        if shift is not None:
            grouper = [pd.Grouper(freq=shift, key=cdate)]
        grouper = grouper + self.groupby

        # Format as datetime
        if cdate is not None:
            aux[cdate] = pd.to_datetime(aux[cdate])

        # ------------------------------------------
        # Frequencies
        # ------------------------------------------
        #
        rn = {
            'mean': 'mari',
            'count': 'freq'
        }

        # Compute frequencies
        isolates = aux.groupby(grouper) \
            .size().unstack().fillna(0)

        # Include mari by isolate
        isolates['mari'] = sari(isolates, **kwargs)

        # Compute frequencies
        if shift is None:

            # Compute mari
            dataframe = isolates.mari\
                .groupby(level=isolates.index.names[:-1]) \
                .agg(['count', 'mean']) \

        else:

            # Create sum and count per shift
            aux = isolates.reset_index() \
                .groupby([cdate] + grouper[1:-2]) \
                .mari.agg(['sum', 'count']) \
                .reset_index().groupby(grouper[1:-2])

            # Compute sums
            sums = aux.rolling(window=period,
                min_periods=1, on=cdate)['sum'].sum()

            # Compute isolate counts
            counts = aux.rolling(window=period,
                min_periods=1, on=cdate)['count'].sum()

            series = (sums/counts).rename('mari')

            dataframe = pd.concat([sums, counts, series], axis=1)

            # Wrong!!
            # Compute sum and count [sum, count]
            #aux = freqs.groupby([cdate] + grouper[2:-1]) \
            #    .mari.agg('mean').reset_index() \
            #    .set_index(cdate).groupby(grouper[2:-1]) \
            #    .mari.rolling(window=period, min_period=1) \
            #    .mean()

        # Rename columns
        dataframe = dataframe.rename(columns=rn)

        # Remove frequencies
        if not return_frequencies:
            dataframe = dataframe['mari']

        # Return
        if return_isolates:
            return dataframe, isolates
        return dataframe
