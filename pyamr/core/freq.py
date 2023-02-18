################################################################################
# Author:
# Date:
# Description:
#
# Copyright:
# 
################################################################################
from __future__ import division

# Libraries
import sys
import numpy as np
import pandas as pd


class Frequency(): # pragma: no cover
    """
    """

    # Attributes
    c_abx = 'ANTIBIOTIC'
    c_org = 'SPECIE'
    c_dat = 'DATE'
    c_out = 'SENSITIVITY'

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------
    def __init__(self, column_antibiotic=c_abx,
                 column_organism=c_org,
                 column_date=c_dat,
                 column_outcome=c_out,
                 column_labnumber=None,
                 dfmt='%Y-%M-%d'):
        """The constructor.

        Parameters
        ----------
        column_antibiotic : string
          The column name with the the antibiotic values

        column_organism : string
          The column name with the organism values

        column_date : string
          The column name with the dates

        column_labnumber : string
          The column name with the laboraory number

        Returns
        -------
        """
        # Create dictionary to rename columns
        self.rename_columns = {column_antibiotic: self.c_abx,
                               column_organism: self.c_org,
                               column_date: self.c_dat,
                               column_outcome: self.c_out}

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------
    def _by_category_groupby(self, by_category='pairs'):
        """This method returns the grouping list.

        Parameters
        ----------
        by_category : string
          The category to group by from pairs, organisms or antibiotics.

        Returns
        -------
        list
        """
        # Define how to return the overall results.
        if by_category == 'organisms':
            return [self.c_org, self.c_out]
        elif by_category == 'antibiotics':
            return [self.c_abx, self.c_out]
        elif by_category == 'pairs':
            return [self.c_org, self.c_abx, self.c_out]
        else:
            raise ValueError("The by_category parameter select must be one of"
                             "the following [pairs, organisms, antibiotics]; "
                             "the value <%s> was found." % by_category)

    def fit(self):
        """
        """
        pass

    def _compute_overall(self, dataframe, by_category='pairs'):
        """This method computes the overall frequency count.

        Parameters
        ----------
        dataframe : dataframe-like
          The dataframe with the microbiology data

        by_category

        Returns
        -------
        dataframe
        """
        # Get the definition of groupby
        groupby = self._by_category_groupby(by_category)
        # Compute results
        return dataframe.groupby(groupby).size().unstack().fillna(0)

    def _compute_independent(self, dataframe, by_category='pairs', fs='1D'):
        """This method computes the independent time intervals frequency.

        Parameters
        ----------
        dataframe:  dataframe-like
          The microbiology dataframe with the following columns.

        by_category: string
          The category to group the outcomes. The outcomes are grouped in pairs
          formed by (organism, antibiotic) by default. However, these can be
          also grouped by organisms or antibiotics.

        fs : string
          The frequency sample (e.g. 1D, 1M, 7D, ...)

        Returns
        -------
        dataframe
        """
        # Format the dataframe to have datetime index
        dataframe = dataframe.reset_index()
        dataframe = dataframe.set_index(self.c_dat)

        # Get the definition of groupby
        groupby = [pd.Grouper(freq=fs)] + self._by_category_groupby(by_category)

        # Compute independent window
        dataframe = dataframe.groupby(groupby).size().unstack().fillna(0)

        # Resample
        dataframe = dataframe.reset_index()
        dataframe = dataframe.set_index(self.c_dat) \
            .groupby([self.c_org, self.c_abx]) \
            .resample(fs).mean() \
            .fillna(0)

        # Return
        return dataframe

    def _compute_overlapping(self, dataframe, by_category='pairs',
                             wshift='1D',
                             wsize='2D'):
        """This method computes the overlapping time intervals frequency

        Parameters
        ----------
        dataframe:  dataframe-like
          The microbiology dataframe with the following columns.

        by_category: string
          The category to group the outcomes. The outcomes are grouped in pairs
          formed by (organism, antibiotic) by default. However, these can be
          also grouped by organisms or antibiotics.

        wshift : string
          The shift between consecutive windows (OTI).

        wsize : integer
          The size of the window (OTI)

        Returns
        -------
        dataframe
        """
        # Format the dataframe to have datetime index
        dataframe = self._compute_independent(dataframe=dataframe,
                                              by_category=by_category,
                                              fs=wshift)

        # Reset index
        dataframe = dataframe.reset_index()

        # Compute rolling window
        dataframe = dataframe.groupby([self.c_org, self.c_abx], as_index=False) \
            .apply(lambda x: x.set_index(self.c_dat) \
                   .rolling(window=wsize).sum()).fillna(0)

        # Drop index level (which appears when executing previous code)
        dataframe.index = dataframe.index.droplevel()


        print(dataframe)
        print(self.c_dat, self.c_org, self.c_abx)

        # Resample
        dataframe = dataframe.reset_index()
        dataframe = dataframe.set_index(self.c_dat) \
            .groupby([self.c_org, self.c_abx]) \
            .resample(wshift).mean() \
            .fillna(0)

        # Return
        return dataframe

    def compute(self, dataframe, strategy='overall',
                by_category='pairs',
                fs=None,
                wshift=None,
                wsize=None):
        """This function computes the frequencies.

        The method allows to compute the overall frequencies, the frequencies for
        independent time intervals (ITI) such as monthly or yearly and the
        frequencies for overlapping time intervals (OTI) in which the parameters
        wshift and wsize need to be specified.

        Parameters
        ----------
        dataframe:  dataframe-like
          The microbiology dataframe with the following columns.

        by_category: string
          The category to group the outcomes. The outcomes are grouped in pairs
          formed by (organism, antibiotic) by default. However, these can be
          also grouped by organisms or antibiotics.

        fs : string
          The frequency sample (e.g. 1D, 1M, 7D, ...)

        wshift : integer
          The shift between consecutive windows (OTI).

        wsize : integer
          The size of the window (OTI)

        Returns
        -------
        dataframe
        """
        # Check that it is a dataframe
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("The instance passed as argument needs to be a pandas "
                            "DataFrame. Instead, a <%s> was found. Please convert "
                            "the input accordingly." % type(dataframe))

        # Rename columns
        dataframe = dataframe.rename(columns=self.rename_columns, copy=True)

        # Ensure date columns has date objects.
        dataframe[self.c_dat] = pd.to_datetime(dataframe[self.c_dat])

        # -----------------------
        # Compute
        # -----------------------
        if strategy == 'overall':
            return self._compute_overall(dataframe=dataframe,
                                         by_category=by_category)

        elif strategy == 'ITI':
            return self._compute_independent(dataframe=dataframe,
                                             by_category=by_category,
                                             fs=fs)

        elif strategy == 'OTI':
            return self._compute_overlapping(dataframe=dataframe,
                                             by_category=by_category,
                                             wshift=wshift,
                                             wsize=wsize)


if __name__ == '__main__': # pragma: no cover

    """
    # Import libraries
    import sys
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    # Import own module
    sys.path.append('../../')

    # Import specific libraries
    from pyAMR.datasets import load

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
    is_org = data['organismCode'] == 'ECOL'
    is_abx = data['antibioticCode'].isin(['ATAZ'])
    data = data[is_abx & is_org]

    # -------------------------
    # Create frequency instance
    # -------------------------
    # Create instance
    freq = Frequency(column_antibiotic='antibioticCode',
                     column_organism='organismCode',
                     column_date='dateReceived',
                     column_outcome='sensitivity')

    # ------------------------
    # Examples compute overall
    # ------------------------
    # Examples compute overall
    pairs = freq.compute(data, by_category='pairs')
    antibiotics = freq.compute(data, by_category='antibiotics')
    organisms = freq.compute(data, by_category='organisms')

    # Show
    # print pairs.head(10)
    # print antibiotics.head(10)
    # print organisms.head(10)

    # -------------------------------------------
    # Examples compute independent time intervals
    # -------------------------------------------
    # Examples compute ITI
    daily = freq.compute(data, strategy='ITI',
                         by_category='pairs',
                         fs='1D')

    monthly = freq.compute(data, strategy='ITI',
                           by_category='pairs',
                           fs='1M')

    # Show
    # print daily.head(10)
    # print monthly.head(10)

    # -------------------------------------------
    # Examples compute overlapping time intervals
    # -------------------------------------------
    # Examples compute OTI (daily)
    oti_1 = freq.compute(data, strategy='OTI',
                         by_category='pairs',
                         wshift='1D',
                         wsize=5)

    # Examples compute OTI (monthly)
    oti_2 = freq.compute(data, strategy='OTI',
                         by_category='pairs',
                         wshift='1M',
                         wsize=2)
    # ----------------
    # Plot
    # ----------------
    # Show comparison for each pair
    f, axes = plt.subplots(4, 1, figsize=(15, 8))

    # Flatten axes
    axes = axes.flatten()

    # Plot ITI (daily)
    for i, (pair, group) in enumerate(daily.groupby(level=[0, 1])):
        group.index = group.index.droplevel([0, 1])
        group.sum(axis=1).plot(marker='o', ms=3, label=pair,
                               linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                               ax=axes[0])

    # Plot ITI (monthly)
    for i, (pair, group) in enumerate(monthly.groupby(level=[0, 1])):
        group.index = group.index.droplevel([0, 1])
        group.sum(axis=1).plot(marker='o', ms=3, label=pair,
                               linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                               ax=axes[1])

    # Plot OTI
    for i, (pair, group) in enumerate(oti_1.groupby(level=[0, 1])):
        group.index = group.index.droplevel([0, 1])
        group.sum(axis=1).plot(marker='o', ms=3, label=pair,
                               linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                               ax=axes[2])

    # Plot OTI
    for i, (pair, group) in enumerate(oti_2.groupby(level=[0, 1])):
        group.index = group.index.droplevel([0, 1])
        group.sum(axis=1).plot(marker='o', ms=3, label=pair,
                               linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                               ax=axes[3])

    # Set legend
    for ax in axes:
        ax.legend()
        ax.set_xlabel('')
        ax.grid(True)

    # Set titles
    axes[0].set_ylabel('Daily')
    axes[1].set_ylabel('Monthly')
    axes[2].set_ylabel('OTI(1D,5)')
    axes[3].set_ylabel('OTI(1M,2)')

    # Show
    plt.show()
    """