# Libraries
import warnings
import pandas as pd

def dri(*args, **kwargs):
    return drug_resistance_index(*args, **kwargs)

def drug_resistance_index_v2(smmry, cu='use', cr='sari',
                          return_all=False,
                          reference_time=None,
                          **kwargs):
        """Computes the Drug Resistance Index

        An possible summary table would look like this...

        DATE     MICROORGANISM ANTIMICROBIAL     sari   use
        2011 Q2  E. Coli       Aminopenicillins  0.422  300
        2011 Q2  E. Coli       Quinolones        0.130  250
        2011 Q2  E. Coli       Cephalosporins    0.010  100
        2011 Q3  E. Coli       Aminopenicillins  0.437  250
        2011 Q3  E. Coli       Quinolones        0.132  300
        2011 Q3  E. Coli       Cephalosporins    0.014  1500


        Parameters
        ----------
        smmry: pd.DataFrame
            The summary DataFrame with the data required to compute the
            drug resistance index. The following information needs to be
            present in the DataFrame:
               (i) the date (e.g. DATE)
               (ii) the resistance (e.g. sari)
               (iii) the drug use (e.g. use)

        cu: str
            Column name with use
        cr: str
            Column name with resistance
        ct: str
            Column name with time
        **kwargs
            Arguments to pass to groupby

        Returns
        -------
        """

        # Enable to chose whether to return all columns or only dri.
        # Ensure that the summary matrix is consistent

        # Clone matrix
        m = smmry.copy(deep=True)

        # Compute
        m['use_period'] = m \
            .groupby(**kwargs)[cu] \
            .transform(lambda x: x.sum())
        m['u_weight'] = (m[cu] / m.use_period)  # .round(decimals=2)
        m['w_rate'] = (m[cr] * m.u_weight)      # .round(decimals=3)
        m['dri'] = m \
            .groupby(**kwargs).w_rate \
            .transform(lambda x: x.sum())

        # Check result for validity.
        #if (m.dri > 1).any():
        #    raise warnings.warn("""
        #            The dri column is ill defined because it has
        ##            values larger than one. Please revisit the
        #            summary table and ensure that all the data
        #            is consistent with the requirements.""")

        """
        if reference_time is not None:
            for t in reference_time:
                # Get use_period uses
                aux = m.groupby(**kwargs).use_period.first()

                use = aux.values[0]
                u_weight = (m[cu] / use)
                w_rate = (m[cr] * u_weight)
                print(w_rate)

                a = m.groupby(**kwargs).groups.keys()
                print(a)
                m['dri_%s' % t] = m \
                    .groupby(**kwargs).w_rate1 \
                    .transform(lambda x: x.sum())

        print(m)
        """

        if return_all:
            return m

        # Update use
        m.use = m.groupby(**kwargs).use \
            .transform(lambda x: x.sum())
        return m.drop(columns=[
            'use_period', 'u_weight', 'w_rate']) \
                .groupby(**kwargs).first()


def drug_resistance_index(dataframe,
            return_complete=False,
            return_usage=False):
    """Computes the DRI.

    .. note:

    Parameters
    ----------

    Returns
    -------
    """
    # Required columns
    required = ['USE', 'RESISTANCE']

    # Check columns
    if set(required).difference(dataframe.columns):
        raise ValueError("The following columns are missing: {0} " \
            .format(set(required).difference(dataframe.columns)))

    # Clone matrix
    m = dataframe.copy(deep=True)

    # Compute
    u, r = m.USE, m.RESISTANCE
    wu = u / u.sum()
    wr = r * wu

    # Return
    if return_complete:
        m['use_period'] = u.sum()
        m['u_weight'] = wu
        m['w_rate'] = wr
        m['dri'] = wr.sum()
        return m
    if return_usage:
        return pd.Series({
            'use_period': u.sum(),
            'dri': wr.sum()
        })
    return wr.sum()



class DRI:
    """

    """
    # Attributes
    c_spe = 'SPECIMEN'
    c_org = 'MICROORGANISM'
    c_abx = 'ANTIMICROBIAL'
    c_dat = 'DATE'
    c_out = 'SENSITIVITY'
    c_drg = 'DRUG'

    c_res = 'RESISTANCE'
    c_use = 'USE'


    """"""
    def __init__(self, column_resistance=c_res,
                       column_usage=c_use):
        """"""
        # Create dictionary to rename columns
        self.rename = {
            column_resistance: self.c_res,
            column_usage: self.c_use
        }

    def compute(self, dataframe, groupby=None,
                column_usage=None, **kwargs):
        """Computes the DRI index.

        .. note:: Include checks.

        Parameters
        ----------
        dataframe: pd.DataFrame
            The pandas dataframe with the information. The following columns
            are always required [RESISTANCE and USE]. The RESISTANCE columns
            indicates the proportion of resistance isolates and the USE the
            amount of antimicrobial doses applied.

        groupby: list, default=None
            The elements to groupby (pd.groupby)

        column_usage: str
            The column with the usage values. This value overwrites the
            column_usage value passed during the instance creation. If
            the value is None, the default value passed during the instance
            creation will be used.

        **kwargs

        Returns
        -------
        """
        # Bad input type
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("""
                The instance passed as argument needs to be a pandas
                DataFrame. Instead, a <%s> was found. Please convert 
                the input accordingly.""" % type(dataframe))

        if isinstance(groupby, str):
            groupby = [groupby]

        # Temporal update of usage column
        rename = self.rename.copy()
        if column_usage is not None:
            rename = {k:v for k,v in rename.items()
                if v != self.c_use}
            rename[column_usage] = self.c_use

        # Rename columns
        aux = dataframe.rename(columns=rename, copy=True)

        # Compute overall
        if groupby is None or not groupby:
            return dri(aux, **kwargs)

        # Compute
        scores = aux.groupby(by=groupby) \
            .apply(dri, **kwargs)

        # Format
        if isinstance(scores, pd.Series):
            scores.rename('dri', inplace=True)

        # Return
        return scores








if __name__ == '__main__':

    # Libraries
    import pandas as pd

    from pathlib import Path

    # ----------------------------------
    # Create data
    # ----------------------------------
    # Define susceptibility test records
    susceptibility_records = [
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

    # Define prescription test records
    prescription_records = [
        ['2021-01-01', 'PATIENT_1', 'AAUG', 150],
        ['2021-01-02', 'PATIENT_1', 'AAUG', 220],
        ['2021-01-03', 'PATIENT_1', 'AAUG', 150],

        ['2021-01-01', 'PATIENT_2', 'AAUG', 250],
        ['2021-01-02', 'PATIENT_2', 'AAUG', 320],
        ['2021-01-03', 'PATIENT_2', 'AAUG', 350],

        ['2021-01-01', 'PATIENT_3', 'ACIP', 450],
        ['2021-01-02', 'PATIENT_3', 'ACIP', 420],
        ['2021-01-03', 'PATIENT_3', 'ACIP', 450],

        ['2021-01-01', 'PATIENT_4', 'ACIP', 50],
        ['2021-01-02', 'PATIENT_4', 'ACIP', 50],
        ['2021-01-03', 'PATIENT_4', 'ACIP', 50],

    ]

    prescription_records = [
        ['2021-01-01', 'PATIENT_1', 'AAUG', 1500],
        ['2021-01-02', 'PATIENT_1', 'AAUG', 2],
        ['2021-01-03', 'PATIENT_1', 'AAUG', 500],

        ['2021-01-01', 'PATIENT_2', 'AAUG', 2000],
        ['2021-01-02', 'PATIENT_2', 'AAUG', 320],
        ['2021-01-03', 'PATIENT_2', 'AAUG', 350],

        ['2021-01-01', 'PATIENT_3', 'ACIP', 2],
        ['2021-01-02', 'PATIENT_3', 'ACIP', 505],
        ['2021-01-03', 'PATIENT_3', 'ACIP', 1124],

        ['2021-01-01', 'PATIENT_4', 'ACIP', 5],
        ['2021-01-02', 'PATIENT_4', 'ACIP', 643],
        ['2021-01-03', 'PATIENT_4', 'ACIP', 2330],

    ]


    # Create DataFrames
    susceptibility = pd.DataFrame(susceptibility_records,
        columns=['DATE',
                 'SPECIMEN',
                 'MICROORGANISM',
                 'ANTIMICROBIAL',
                 'SENSITIVITY'])

    prescriptions = pd.DataFrame(prescription_records,
        columns=['DATE',
                 'PATIENT',
                 'DRUG',
                 'DOSE'])

    # Format dates
    susceptibility.DATE = pd.to_datetime(susceptibility.DATE)
    prescriptions.DATE = pd.to_datetime(prescriptions.DATE)

    # Show
    print("\nSusceptibility records")
    print(susceptibility.head(5))
    print("\nPrescription records")
    print(prescriptions.head(5))


    # .. note:: Uncomment to load the CDDEP example data instead

    # Load default CDDEP sample
    #path = Path('../datasets/cddep')
    #susceptibility = pd.read_csv(path / 'susceptibility.csv')
    #prescriptions = pd.read_csv(path / 'prescriptions.csv')


    # ------------------------
    # Compute summary table
    # ------------------------
    # Libraries
    from pyamr.core.sari import SARI

    # Create sari instance
    sari = SARI(groupby=['DATE',
                         'SPECIMEN',
                         'MICROORGANISM',
                         'ANTIMICROBIAL',
                         'SENSITIVITY'])

    # Compute susceptibility summary table
    smmry1 = sari.compute(susceptibility,
        return_frequencies=False)

    # Compute prescriptions summary table.
    smmry2 = prescriptions \
        .groupby(by=['DATE', 'DRUG']) \
        .DOSE.sum().rename('use')

    # Combine both summary tables
    smmry = smmry1.reset_index().merge(
        smmry2.reset_index(), how='inner',
        left_on=['DATE', 'ANTIMICROBIAL'],
        right_on=['DATE', 'DRUG']
    )

    # Show
    print("\nSummary")
    print(smmry)


    # -------------------------
    # Compute DRI
    # -------------------------
    obj = DRI(
        column_resistance='sari',
        column_usage='use'
    )

    # Compute DRI overall
    dri1 = obj.compute(smmry)

    # Compute DRI
    dri2 = obj.compute(smmry,
        groupby=['SPECIMEN'])

    # Compute DRI
    dri3 = obj.compute(smmry,
        groupby=['MICROORGANISM'])

    # Compute DRI
    dri4 = obj.compute(smmry,
        groupby=['MICROORGANISM', 'ANTIMICROBIAL'])

    # Compute DRI
    dri5 = obj.compute(smmry,
        groupby=['DATE'],
        return_usage=True)

    # Compute DRI
    dri6 = obj.compute(smmry,
        groupby=['DATE', 'MICROORGANISM'],
        return_usage=True)

    # Compute DRI
    dri7 = obj.compute(smmry,
        groupby=['DATE', 'MICROORGANISM', 'ANTIMICROBIAL'],
        return_usage=True,
        return_complete=True)

    # Compute DRI (return all elements of summary table).
    dri8 = obj.compute(smmry,
        groupby=['MICROORGANISM'],
        return_complete=True)

    # Show
    print("\nDRI (1):")
    print(dri1)
    print("\nDRI (2):")
    print(dri2)
    print("\nDRI (3):")
    print(dri3)
    print("\nDRI (4):")
    print(dri4)
    print("\nDRI (5):")
    print(dri5)
    print("\nDRI (6):")
    print(dri6)
    print("\nDRI (7):")
    print(dri7)
    print("\nDRI (8):")
    print(dri8)


    # --------------------------------------------
    # Compute DRI fixed
    # --------------------------------------------
    # Compute prescriptions on t0.
    use_t0 = prescriptions \
        .groupby(by=['DATE', 'DRUG']) \
        .DOSE.sum().rename('use') \
        .to_frame().reset_index() \
        .groupby('DRUG').use.first()

    # Add to summary table
    smmry = smmry.assign(use_t0=smmry.DRUG.map(use_t0))

    # Define groupby
    groupby = [
        'DATE',
        'MICROORGANISM'
    ]

    # Compute DRI
    dri9a = obj.compute(smmry,
        groupby=groupby,
        return_usage=True)

    # Compute DRI using new USE
    dri9b = obj.compute(smmry,
        groupby=groupby,
        return_usage=True,
        column_usage='use_t0')

    #aux = pd.concat([dri9a, dri9b], axis=1)
    aux = dri9a.merge(dri9b,
        left_index=True, right_index=True,
        suffixes=['', '_fixed'])

    # Concatenate (series)
    #aux = pd.concat([
    #    dri9a.rename('dri'),
    #    dri9b.rename('dri_fixed')], axis=1)

    # Show
    print("\n\n")
    print("\nSummary (variable):")
    print(smmry)
    print("\nDRI (9):")
    print(aux)


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

    """
    # Compute DRI overall
    dri1 = dri(smmry)

    # Compute DRI
    dri8 = smmry \
        .groupby(by=['SPECIMEN']) \
        .apply(drug_resistance_index_v2)

    # Compute DRI
    dri2 = smmry \
        .groupby(by=['MICROORGANISM']) \
        .apply(drug_resistance_index_v2)

    dri3 = smmry \
        .groupby(by=['MICROORGANISM', 'ANTIMICROBIAL']) \
        .apply(drug_resistance_index_v2,
               return_components=True)

    # Compute DRI
    dri9 = smmry \
        .groupby(by=['DATE']) \
        .apply(drug_resistance_index_v2)

    dri4 = smmry \
        .groupby(by=['DATE', 'MICROORGANISM']) \
        .apply(drug_resistance_index_v2,
               return_components=True)

    dri5 = smmry \
        .groupby(by=['DATE', 'MICROORGANISM', 'ANTIMICROBIAL']) \
        .apply(drug_resistance_index_v2,
               return_components=True)
    """

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


    """
    # -------------------------
    # Compute resistance index
    # -------------------------
    r = drug_resistance_index(smmry,
        by=['DATE'],
        return_all=True,
        reference_time=[1,2])

    # Show
    print("\nResult:")
    print(r.round(decimals=3))
    """