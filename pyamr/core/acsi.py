# Libraries
import numpy as np
import pandas as pd


def create_combinations_v1(d, groupby,
                              col_spe='SPECIMEN',
                              col_lab='LAB_NUMBER',
                              col_org='MICROORGANISM',
                              col_abx='ANTIMICROBIAL',
                              col_sns='SENSITIVITY'):
    """Creates the DataFrame with all combinations.

    .. note:: There might be an issue if there are two different outcomes
              for the same record. For example, a susceptibility test
              record for penicillin (APEN) with R and another one with
              S. Warn of this issue if it appears!

    .. note:: If the data is right and the laboratory numbers are unique per
              isolate then the date is not necessary. However, what if we want
              to keep it? Groupby should at least contain:
                    specimen, microorganism and lab_id

    .. note:: How to add all data in addition to the columns manually.

    Parameters
    ----------

    Returns
    --------
    """
    # Libraries
    from itertools import combinations

    # Initialize
    c = []

    # Loop
    for i, g in d.groupby(groupby):
        for x, y in combinations(g.sort_values(by=col_abx).index, 2):
            aux = dict(zip(groupby, i))

            aux.update({
                '%s_x' % col_abx: g.loc[x, col_abx],
                '%s_y' % col_abx: g.loc[y, col_abx],
                '%s_x' % col_sns: g.loc[x, col_sns],
                '%s_y' % col_sns: g.loc[y, col_sns]
            })
            c.append(aux)

    # Create DataFrame
    c = pd.DataFrame(c)

    # Add class
    c['class'] = c['%s_x' % col_sns] + \
                 c['%s_y' % col_sns]
    # Return
    return c






def mutual_info_matrix_v3(x=None, y=None, ct=None):
    """Compute the component information score.

    .. note: Might be inefficient but good for testing.

    .. note: In order to be able to compute the mutual
             information score it is necessary to have
             variation within the variable. Thus, if
             there is only one class, should we return
             a result or a warning?

    Parameters
    ----------
    x: list
        List with the classes
    y: list
        List with the classes

    Returns
    -------
    """
    # Libraries
    from scipy.stats.contingency import crosstab

    def _check_nparray(obj, param_name):
        if obj is not None:
            if isinstance(obj, np.ndarray):
                return obj
            elif isinstance(obj, pd.Series):
                return obj.to_numpy()
            elif isinstance(obj, pd.DataFrame):
                return obj.to_numpy()
            elif isinstance(obj, list):
                return np.array(obj)
            else:
                raise ValueError("""
                       The input parameter '{0}' is of type '{1} which is 
                       not supported. Please ensure it is a np.ndarray."""
                                 .format(param_name, type(obj)))

    # Ensure they are all np arrays
    x = _check_nparray(x, 'x')
    y = _check_nparray(y, 'y')
    ct = _check_nparray(ct, 'ct')

    # Compute contingency
    if ct is None:
        c = crosstab(x,y)
        if isinstance(c, tuple):
            ct = c[-1]   # older scipy
        else:
            ct = c.count # newer scipy

    # Variables
    n = ct.sum()
    pi = np.ravel(ct.sum(axis=1)) / n
    pj = np.ravel(ct.sum(axis=0)) / n

    # Create empty matrix
    m = np.empty(ct.shape)
    m[:] = np.nan

    # Fill with component information score
    with np.errstate(all='ignore'):
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                pxy = ct[i,j] / n
                m[i,j] = pxy * np.log(pxy / (pi[i] * pj[j]))

    # Fill with na (lim x->0 => 0)
    m[np.isnan(m)] = 0

    # Return
    return m


def collateral_resistance_index(m):
    """Collateral Resistance Index

    The collateral resistance index is based on the mutual
    information matrix. This implementation assumes there
    are only two classes resistant (R) and sensitive (S).

    .. warning:: Only works for a 2x2 contingency matrix

    Parameters
    ----------
    m: np.array
        A numpy array with the mutual information matrix.
        Also called the contingency matrix.

    Returns
    -------
    """
    return (m[0, 0] + m[1, 1]) - (m[0, 1] + m[1, 0])


def CRI(x, func_mis=mutual_info_matrix_v3):
    """Collateral resistance index

    Parameters
    ----------
    x: pd.Series
        Contains the combinations classes (e.g. SS, SR, RS, RR)

    func_mis: function
        The function to use to compute the contingency matrix from the
        mutual information score. By default it uses the function
        mutual_info_matrix_v3.
    """
    ct = np.array([[x.SS, x.SR], [x.RS, x.RR]])
    m = func_mis(ct=ct)
    return collateral_resistance_index(m)



class ACSI:
    """
    Antimicrobial Collateral Sensitivity Index

    How should we call this index?
       a) Antimicrobial Disjoint Resistance Index
       b) Antimicrobial Collateral Resistance Index
       c) Antimicrobial Collateral Sensitivity Index
       d) Antimicrobial Collateral Resistance Index

    """

    # Attributes
    c_spe = 'SPECIMEN'
    c_org = 'MICROORGANISM'
    c_abx = 'ANTIMICROBIAL'
    c_sns = 'SENSITIVITY'
    c_lab = 'LAB_NUMBER'
    c_dat = 'DATE'

    def __init__(self,
                 column_specimen=c_spe,
                 column_microorganism=c_org,
                 column_antimicrobial=c_abx,
                 column_sensitivity=c_sns,
                 column_laboratory=c_lab):
        """The constructor.

        Parameters
        ----------
        column_specimen: string
            The column name with the specimen

        column_antimicrobial: string
            The column name with the antimicrobial

        column_microorganism: string
            The column name with the microorganism

        column_sensitivity: string
            The column name with the sensitivity

        column_laboratory: string
            The column name with the laboratory id

        Returns
        -------
        none
        """

        # Create dictionary to rename columns
        self.rename_columns = {column_specimen: self.c_spe,
                               column_antimicrobial: self.c_abx,
                               column_microorganism: self.c_org,
                               column_sensitivity: self.c_sns,
                               column_laboratory: self.c_lab}


    def combinations(self, dataframe, **kwargs):
        """Creates the combinations.

        .. note:: In theory the combinations only need to be grouped
                  by laboratory number, however, in order to maintain
                  the rest of the information (like date) we need to
                  pass all of them.
        """
        return create_combinations_v1(dataframe, **kwargs)

    def compute(self, dataframe,
                flag_combinations=False,
                groupby=None,
                func_mis=None,
                return_combinations=False):
        """Computes the antimicrobial collateral sensitivity index.

        .. note:: Enable to pass a combinations dataframe.
        .. note:: The lab number should be used only to compute
                  the combinations. It should not be used when
                  computing the ACSI.

        Parameters
        ----------
        dataframe: pd.DataFrame
            A dataframe with the susceptibility test interpretations as columns.

        combinations: boolean
            Indicates whether the variable DataFrame contains susceptibility
            test records (combinations=False) or the antimicrobial combinations
            and the class (combination=True)

        func_mis: function
            The function to use to compute the contingency matrix from the
            mutual information score. By default it uses the function
            mutual_info_matrix_v3.

        Returns
        -------
        pd.Series or pd.DataFrame

        """

        # Do checks

        # Set default groupby
        if groupby is None:
            groupby = [
                self.c_dat,
                self.c_spe,
                self.c_org,
            ]

        # Set default function
        if func_mis is None:
            func_mis = mutual_info_matrix_v3

        # Rename columns
        aux = dataframe.copy(deep=True) \
            .rename(columns=self.rename_columns)

        # Create combinations
        if flag_combinations:
            combinations = aux
        else:
            combinations = self.combinations(aux,
                groupby=groupby + [self.c_lab])

        # Create contingency DataFrame
        contingency = combinations.groupby(
            by=groupby + [
                self.c_abx + '_x',
                self.c_abx + '_y',
                'class'])\
            .size().unstack()

        # Ensure that variables in CRI needed exist
        for s in ['SS', 'RS', 'SR', 'RR']:
            if not s in contingency:
                contingency[s] = 0

        # Compute CRI
        contingency['acsi'] = contingency.fillna(0) \
            .apply(CRI, args=(func_mis,), axis=1)

        # Return
        if return_combinations:
            return contingency, combinations
        return contingency





if __name__ == '__main__':

    # Libraries
    import pandas as pd

    # ----------------------------------
    # Create data
    # ----------------------------------
    # Define susceptibility test records
    susceptibility_records = [
        ['2021-01-01', 'LAB_1', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
        ['2021-01-01', 'LAB_1', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],

        ['2021-01-01', 'LAB_2', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
        ['2021-01-01', 'LAB_2', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],

        ['2021-01-01', 'LAB_3', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
        ['2021-01-01', 'LAB_3', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],

        ['2021-01-01', 'LAB_4', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
        ['2021-01-01', 'LAB_4', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],

        ['2021-01-02', 'LAB_5', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
        ['2021-01-02', 'LAB_5', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],

        ['2021-01-02', 'LAB_6', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
        ['2021-01-02', 'LAB_6', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],

        ['2021-01-02', 'LAB_7', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
        ['2021-01-02', 'LAB_7', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],

        ['2021-01-03', 'LAB_8', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
        ['2021-01-03', 'LAB_8', 'BLDCUL', 'ECOL', 'ACIP', 'intermediate'],

        ['2021-01-03', 'LAB_9', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
        ['2021-01-03', 'LAB_9', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
        ['2021-01-03', 'LAB_9', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
        ['2021-01-03', 'LAB_9', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],

        ['2021-01-04', 'LAB_10', 'URICUL', 'ECOL', 'AAUG', 'resistant'],
        ['2021-01-04', 'LAB_10', 'URICUL', 'ECOL', 'ACIP', 'sensitive'],
        ['2021-01-04', 'LAB_10', 'URICUL', 'SAUR', 'AAUG', 'resistant'],
        ['2021-01-04', 'LAB_10', 'URICUL', 'SAUR', 'APEN', 'resistant'],
    ]

    # Create DataFrames
    susceptibility = pd.DataFrame(susceptibility_records,
        columns=['DATE',
                 'LAB_NUMBER',
                 'SPECIMEN',
                 'MICROORGANISM',
                 'ANTIMICROBIAL',
                 'SENSITIVITY'])

    # Format DataFrame
    susceptibility.SENSITIVITY = \
        susceptibility.SENSITIVITY.replace({
            'resistant': 'R',
            'intermediate': 'I',
            'sensitive': 'S'
    })

    # Show
    print("\nSusceptibility:")
    print(susceptibility)

    # .. note: It is important to ensure that there are not susceptibility
    #          test records with contradicting results. For example being
    #          resistant and sensitive at the same time. Integrate this
    #          check in the computation!

    # ---------------------------
    # Create combinations
    # ---------------------------
    # Create combinations
    c = create_combinations_v1(susceptibility,
        groupby=[
            'DATE',
            'LAB_NUMBER',
            'SPECIMEN',
            'MICROORGANISM'
        ])

    print("\nCombinations:")
    print(c)

    # Build contingency
    r = c.groupby([
        'DATE',
        'SPECIMEN',
        'MICROORGANISM',
        'ANTIMICROBIAL_x',
        'ANTIMICROBIAL_y',
        'class']).size().unstack()

    print("Contingency:")
    print(r)

    # Compute CRI
    r['MIS'] = r.fillna(0) \
        .apply(CRI, args=(mutual_info_matrix_v3,), axis=1)

    # Show
    print("\nResult")
    print(r)


    # ------------------------------------------
    # Computes ACSI using class
    # ------------------------------------------

    def show(combinations, contingency, title=None, n=100):
        """Helper function to display outcomes."""
        # Variables
        n_comb = combinations.shape[0]
        n_cont = np.nansum(contingency.to_numpy()[:, :-1])

        if title is None:
            title = 'Grouped By: %s' % str(contingency.index.names[:-2])

        # Display
        print("\n" + "="*n + '\n%s\n'%title + "="*n)
        print("Total combinations: %s" % int(n_comb))
        print("Total contingency:  %s" % int(n_cont))
        print("\nCombinations:")
        print(combinations)
        print("\nContingency:")
        print(contingency)


    # Create ACSI instance
    acsi = ACSI()

    # ---------------
    # Compute overall
    # ---------------
    # .. note:: Why removing LAB_NUMBER returns only
    #           the first letter...?
    # Compute index
    contingency, combinations = \
        acsi.compute(susceptibility,
                     groupby=[],
                     return_combinations=True)

    # Show
    show(combinations, contingency, title='Overall')


    # ---------------
    # Compute by
    # ---------------
    # Compute index
    contingency, combinations = \
        acsi.compute(susceptibility,
                     groupby=['DATE'],
                     return_combinations=True)

    # Show
    show(combinations, contingency, title='By <DATE>')


    # ----------------
    # Compute by pairs
    # ----------------
    # Compute index
    contingency, combinations = \
        acsi.compute(susceptibility,
            groupby=[
                'SPECIMEN',
                'MICROORGANISM'
            ],
            return_combinations=True)

    # Show
    show(combinations, contingency, title='By <SPECIMEN, MICROORGANISM>')

    # -------------------------
    # Compute by date and pairs
    # -------------------------
    # .. note:: It seems that it is important to include all the
    #           parameters when computing the combinations. Otherwise
    #           it might create ill defined combinations. Think this
    #           through...

    # Compute index
    contingency, combinations = \
        acsi.compute(susceptibility,
            groupby=[
                 'DATE',
                 'SPECIMEN',
                 'MICROORGANISM'
            ],
            return_combinations=True)

    # Show
    show(combinations, contingency, title=None)

    # Compute contingency reusing combinations.
    contingency = acsi.compute(combinations.reset_index(),
        groupby=['SPECIMEN'],
        flag_combinations=True,
        return_combinations=False)
    show(combinations, contingency, title=None)

    # Compute contingency reusing combinations.
    contingency = acsi.compute(combinations.reset_index(),
        groupby=['MICROORGANISM'],
        flag_combinations=True,
        return_combinations=False)
    show(combinations, contingency, title=None)



    # -------------------------------------------------------------------------
    # Testing
    # -------------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # Success
    # ---------------------------------------------------------------------
    # .. note: All this examples should succeed. At the moment the code
    #          breaks if gram is not included. This is because the data
    #          we have created has duplicated values for each gram.
    #          Should we consider this within the ASAI?

    # ---------------------------------------------------------------------
    # Errors
    # ---------------------------------------------------------------------
    # .. note: In the examples below, the method acsi is meant to raise
    #          an error either because any of the required missing columns
    #          is missing or because the configuration is not correct.
    print("\n\nHandling errors:")

    # ---------------------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------------------
    # .. note: In the examples below, the method acsi is meant to show a
    #          warning message either no threshold has been specified or
    #          because thresholds have been specified twice.
    print("\n\nShow warnings:")