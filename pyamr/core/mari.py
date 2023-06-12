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
    """Multiple Antimicrobial Resistance Index"""
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
            The labels of the columns to groupby. The name of
            the columns it should include is as follows:

                [
                    COLUMN_SPECIMEN,
                    COLUMN_MICROORGANISM,
                    COLUMN_LABORATORY_NUMBER,
                    COLUMN_OUTCOME
                ]

        Returns
        --------
        MARI instance
        """
        self.groupby = groupby


    def compute_v1(self, dataframe, shift=None, period=None,
                 cdate=None, return_frequencies=True,
                 return_isolates=True, **kwargs): # pragma: no cover
        """"""
        # Copy DataFrame
        aux = dataframe.copy(deep=True)

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
            dataframe = isolates.mari \
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


    def rolling(self, dataframe, period, cdate, shift=None):
        """"""
        if shift is None:
            warnings.warn("""
                The input parameter <shift> is None. Thus, the value 
                of the input parameter <period> (%s) has been used."""
                % period)
            shift = period

        # Grouper
        grouper = [pd.Grouper(freq=shift, key=cdate)]
        grouper = grouper + self.groupby[:-2]

        # Compute frequencies
        freqs = dataframe.groupby(grouper) \
            .agg(intermediate=('intermediate', 'sum'),
                 resistant=('resistant', 'sum'),
                 sensitive=('sensitive', 'sum'),
                 n_records=('freq', 'sum'),
                 n_samples=('sari', 'count'),
                 total=('sari', 'sum')) \
            .reset_index() \
            .set_index(cdate).groupby(grouper[1:]) \
            .rolling(window=period, min_periods=1) \
            .sum().fillna(0)

        # Return
        return freqs


    def grouping(self, dataframe, period, cdate):
        """Groups the data.
        """
        # Create grouper
        if hasattr(dataframe[cdate].dt, str(period)):
            grouper = [getattr(dataframe[cdate].dt, period)]
        else:
            grouper = [pd.Grouper(freq=period, key=cdate)]
        grouper = self.groupby[:-2] + grouper

        # Compute
        freqs = dataframe.groupby(grouper) \
            .agg(intermediate=('intermediate', 'sum'),
                 resistant=('resistant', 'sum'),
                 sensitive=('sensitive', 'sum'),
                 n_records=('freq', 'sum'),
                 n_samples=('sari', 'count'),
                 total=('sari', 'sum'))

        # Return
        return freqs


    def compute_v2(self, dataframe, shift=None, period=None,
                         cdate=None, return_frequencies=True,
                         return_isolates=True, **kwargs):
        """Compute MARI v2.

        .. note: No need to copy because SARI does it for us
        """
        # Libraries
        from pyamr.core.sari import SARI

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

        # Compute frequencies
        if period is None and shift is None:

            # Compute freqs from sari
            freqs = SARI(groupby=self.groupby) \
                .compute(dataframe,  **kwargs) \
                .groupby(level=[0,1]) \
                .agg(intermediate=('intermediate', 'sum'),
                     resistant=('resistant', 'sum'),
                     sensitive=('sensitive', 'sum'),
                     n_records=('freq', 'sum'),
                     n_samples=('sari', 'count'),
                     total=('sari', 'sum'))

        else:
            # Format as datetime
            dataframe[cdate] = pd.to_datetime(dataframe[cdate])

            # Define new group by with date
            groupby = self.groupby.copy()
            groupby.insert(3, cdate)

            # Compute mari (sari per sample)
            iso = SARI(groupby=groupby) \
                .compute(dataframe, **kwargs) \
                .reset_index()

            if shift is None:
                freqs = self.grouping(dataframe=iso,
                                      period=period,
                                      cdate=cdate)
            else:
                freqs = self.rolling(dataframe=iso,
                                     period=period,
                                     shift=shift,
                                     cdate=cdate)

        # Add mari
        freqs['mari'] = freqs.total / freqs.n_samples

        # Remove frequencies
        if not return_frequencies:
            freqs = freqs['mari']

        # Return
        if return_isolates:
            return freqs, pd.DataFrame()
        return freqs



    def compute_v3(self, dataframe, shift=None, period=None,
                         cdate=None, return_frequencies=True,
                         return_isolates=True, **kwargs): # pragma: no cover
        """Compute MARI v2.

        .. note: It does not work properly.

        .. note: It is considerably slower. Possibly because it
                 is executing the rolling method twice. Try to
                 remove the first rolling as it is not needed.
        """
        # Libraries
        from pyamr.core.sari import SARI

        # Format as datetime
        if cdate is not None:
            dataframe[cdate] = pd.to_datetime(dataframe[cdate])


        # Create object
        sari = SARI(groupby=['SPECIMEN',
                             'MICROORGANISM',
                             'LAB_NUMBER',
                             'DATE',
                             'SENSITIVITY'])

        # Compute mari (sari per sample)
        isolates = sari.compute(dataframe,
            #shift=shift, period=period, cdate=cdate,
            return_frequencies=return_frequencies, **kwargs)

        """
        from pyamr.core.sari import sari
        # Compute frequencies
        isolates = dataframe.groupby(['SPECIMEN',
                             'MICROORGANISM',
                             'LAB_NUMBER',
                             'DATE',
                             'SENSITIVITY']) \
            .size().unstack().fillna(0)

        # Include mari which is the SARI per isolate
        isolates['sari'] = sari(isolates, **kwargs)
        print(isolates)
        """

        by = ['SPECIMEN', 'MICROORGANISM']
        if cdate is not None:
            by = by + [cdate]

        aux = isolates.reset_index() \
            .groupby(by) \
            .agg(intermediate=('intermediate', 'sum'),
                 resistant=('resistant', 'sum'),
                 sensitive=('sensitive', 'sum'),
                 #n_records=('freq', 'sum'),
                 n_samples=('sari', 'count'),
                 total=('sari', 'sum'))

        if period is not None:
            # Compute rolling
            aux = aux \
                .reset_index() \
                .groupby(by[:2]) \
                .rolling(window=period,
                         min_periods=1, on=cdate).agg('sum')

            # Format result.
            aux.index = aux.index.droplevel(2)
            aux = aux.reset_index() \
                .set_index(by)

        # Add mari
        aux['mari'] = aux.total / aux.n_samples

        # Add number of records
        aux['n_records'] = \
            aux.resistant + \
            aux.sensitive + \
            aux.intermediate

        # Return
        if return_isolates:
            return aux, isolates
        return aux


    def compute_v4(self, dataframe, shift=None, period=None,
                         cdate=None, return_frequencies=True,
                         return_isolates=True, **kwargs): # pragma: no cover
        """Compute MARI v1.
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
        # Compute frequencies
        isolates = aux.groupby(grouper) \
            .size().unstack().fillna(0)

        # Include mari which is the SARI per isolate
        isolates['mari'] = sari(isolates, **kwargs)



        # Compute frequencies
        if shift is None:

            # Compute mari
            #dataframe = isolates.mari \
            #    .groupby(level=isolates.index.names[:-1]) \
            #    .agg(['count', 'mean']) \


            dataframe = isolates \
                .groupby(level=isolates.index.names[:-1]) \
                .agg(
                    intermediate=('intermediate', 'sum'),
                    resistant=('resistant', 'sum'),
                    sensitive=('sensitive', 'sum'),
                    n_samples=('mari', 'count'),
                    total=('mari', 'sum')
                )

        else:

            dataframe = isolates.reset_index() \
                .groupby([cdate] + grouper[1:-2]) \
                .agg(intermediate=('intermediate', 'sum'),
                     resistant=('resistant', 'sum'),
                     sensitive=('sensitive', 'sum'),
                     n_samples=('mari', 'count'),
                     total=('mari', 'sum')) \
                .reset_index().groupby(grouper[1:-2]) \
                .rolling(window=period,
                         min_periods=1, on=cdate).agg('sum')

            # Format result.
            dataframe.index = dataframe.index.droplevel(2)
            dataframe = dataframe.reset_index() \
                .set_index(['SPECIMEN',
                            'MICROORGANISM',
                            'DATE'])
        # Add mari
        dataframe['mari'] = dataframe.total / dataframe.n_samples

        # Add number of records
        dataframe['n_records'] = \
            dataframe.resistant + \
            dataframe.sensitive + \
            dataframe.intermediate

        # Remove frequencies
        if not return_frequencies:
            dataframe = dataframe['mari']

        # Return
        if return_isolates:
            return dataframe, isolates
        return dataframe


    def compute(self, dataframe, **kwargs):
        """Compute the Multiple Antimicrobial Resistance Index.

        .. note: The compute_v3 does not work properly

        .. todo: Add parameters to rolling!
        .. todo: Place value at the left, center, right of window?
        .. todo: Ensure that works when time gaps present!
        .. todo: Carefull with various indexes!
        .. todo: Warning if dates NaN
        .. todo: Warning if elements in groupby any all NaN!
        .. todo: Warning if not all samples have been tested with same antimicrobials

        Parameters
        ----------
        dataframe: pd.DataFrame
            A DataFrame with the susceptibility test interpretations
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
        #self.compute_v1(dataframe, **kwargs)
        #self.compute_v2(dataframe, **kwargs)
        #self.compute_v3(dataframe, **kwargs)
        return self.compute_v2(dataframe, **kwargs)


if __name__ == '__main__': # pragma: no cover

    # Import libraries
    import time
    import warnings
    import pandas as pd

    from timeit import default_timer as timer

    # Import specific libraries
    from pyamr.core.mari import MARI

    # Filter user warning
    warnings.filterwarnings("ignore", category=UserWarning)



    # ---------------------
    # Create data
    # ---------------------
    # Load data
    data = pd.read_csv('../fixtures/indexes/fixture_mari.csv')


    # Create MARI instance
    mari = MARI(groupby=['SPECIMEN',
                         'MICROORGANISM',
                         'LAB_NUMBER',
                         'SENSITIVITY'])

    # Compute MARI overall
    mari_overall, isolates = mari.compute(data,
        return_frequencies=True,
        return_isolates=True)

    # Compute SARI temporal (ITI)
    mari_iti_1d_1d = mari.compute(data, shift='1D',
        period='1D', cdate='DATE',
        return_isolates=False)

    mari_iti_2d_2d = mari.compute(data, shift='2D',
        period='2D', cdate='DATE',
        return_isolates=False)

    mari_iti_year = mari.compute(data,
        period='year', cdate='DATE',
        return_isolates=False)

    # Compute MARI temporal (OTI)
    mari_oti_1d_2d = mari.compute(data, shift='1D',
        period='2D', cdate='DATE',
        return_isolates=False)

    mari_oti_2d_4d = mari.compute(data, shift='2D',
        period='4D', cdate='DATE',
        return_isolates=False)

    # Show
    print("\nIsolates:")
    print(isolates)
    print("\n\n\nMARI (overall):")
    print(mari_overall)
    print("\n\n\nMARI (iti) | 1D_1D:")
    print(mari_iti_1d_1d)
    print("\n\n\nMARI (iti) | 2D_2D:")
    print(mari_iti_2d_2d)
    print("\n\n\nMARI (iti) | year:")
    print(mari_iti_year)
    print("\n\n\nMARI (oti) | 1D_2D:")
    print(mari_oti_1d_2d)
    print("\n\n\nMARI (oti) | 2D_4D:")
    print(mari_oti_2d_4d)


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
              (i + 1, len(combos), shift, period), end="")
        try:
            s00, s01 = mari.compute(data, shift=shift, period=period, cdate='DATE')
            s10, s11 = mari.compute_v2(data, shift=shift, period=period, cdate='DATE')
            s20, s21 = mari.compute_v3(data, shift=shift, period=period, cdate='DATE')
            print("Ok! equals_1=%s equals_2=%s" %
                  (s00.equals(s10), s10.equals(s20)))
            #print(s00)
            #print(s10)
            #print(s20)
            #print("\n\n" + "=" * 80)
        except Exception as e:
            print(e)


    # ---------------------------------------------------
    # Test timings
    # ---------------------------------------------------
    # Libraries
    from pyamr.datasets.load import make_susceptibility

    # Constants
    rename = {
        'date_received': 'DATE',
        'laboratory_number': 'LAB_NUMBER',
        'specimen_code': 'SPECIMEN',
        'microorganism_code': 'MICROORGANISM',
        'antimicrobial_code': 'ANTIMICROBIAL',
        'sensitivity': 'SENSITIVITY'
    }

    # Load data
    data = make_susceptibility()
    data = data.rename(columns=rename)

    print("\n\nComparing execution times:")

    # Example 1
    # =========
    t0 = timer()
    mari_overall, isolates = mari.compute(data,
        return_frequencies=True,
        return_isolates=True)
    t1 = timer()
    mari_overall, isolates = mari.compute_v2(data,
        return_frequencies=True,
        return_isolates=True)
    t2 = timer()
    mari_overall, isolates = mari.compute_v3(data,
        return_frequencies=True,
        return_isolates=True)
    t3 = timer()
    print("%.10f | %.10f | %.10f " % (t1-t0, t2-t1, t3-t2))


    # Example 2
    # =========
    t0 = timer()
    mari_iti = mari.compute(data, shift='1D',
        period='1D', cdate='DATE',
        return_isolates=False)
    t1 = timer()
    mari_iti = mari.compute_v2(data, shift='1D',
        period='1D', cdate='DATE',
        return_isolates=False)
    t2 = timer()
    mari_iti = mari.compute_v3(data, shift='1D',
        period='1D', cdate='DATE',
        return_isolates=False)
    t3 = timer()
    print("%.10f | %.10f | %.10f " % (t1-t0, t2-t1, t3-t2))

    # Example 3
    # =========
    t0 = timer()
    mari_oti = mari.compute(data, shift='1D',
        period='2D', cdate='DATE',
        return_isolates=False)
    t1 = timer()
    mari_oti = mari.compute_v2(data, shift='1D',
        period='2D', cdate='DATE',
        return_isolates=False)
    t2 = timer()
    mari_oti = mari.compute_v3(data, shift='1D',
        period='2D', cdate='DATE',
        return_isolates=False)
    t3 = timer()
    print("%.10f | %.10f | %.10f " % (t1-t0, t2-t1, t3-t2))



