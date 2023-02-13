

# -------------------------------------------
# Methods
# -------------------------------------------
def create_registry(data, keyword=None, keep=None):
    """Creates registry from data.

    Parameters
    ----------
    data: pd.DataFrame
        The data

    keyword: string
        The keyword for the columns. All columns starting
        with such keyword will be kept and used for the
        registry.

    keep: list
        The list of columns to keep for the registry
    """
    # Columns to keep
    if keep is None:
        keep = [c for c in data.columns
            if c.startswith(keyword)]

    # Copy data
    reg = data[keep].copy(deep=True)
    reg = reg.drop_duplicates()
    reg = reg.reset_index(drop=True)

    # Add id
    if keyword is not None:
        reg['%s_id' % keyword] = reg.index.values

    # Return
    return reg




if __name__ == '__main__':

    # Libraries generic
    import time
    import pandas as pd

    # Libraries specific
    from pyamr.datasets.load import make_susceptibility
    from pyamr.datasets.load import load_data_nhs

    # -------------------------------------------
    # Load data
    # -------------------------------------------
    # Load data
    data = make_susceptibility()
    data, abxs, orgs = \
        load_data_nhs(folder='susceptibility-v0.0.5')

    # Show
    print("\nData:")
    print(data)
    print("\nColumns:")
    print(data.columns)

    # --------------------------------------------
    # Create registries
    # --------------------------------------------
    # Create registries
    reg_patient = create_registry(data, keyword='patient')
    reg_specimen = create_registry(data, keyword='specimen')
    reg_sensitivity = create_registry(data, keyword='sensitivity')
    reg_method = create_registry(data, keyword='method')
    reg_microorganism = create_registry(data, keyword='microorganism')
    reg_antimicrobial = create_registry(data, keyword='antimicrobial')

    # Show
    print("\nMethod:")
    print(reg_method)
    print("\nSensitivity:")
    print(reg_sensitivity)
    print("\nSpecimen:")
    print(reg_specimen)
    print("\nMicroorganism:")
    print(reg_microorganism)
    print("\nAntimicrobial:")
    print(reg_antimicrobial)
    print("\nPatients:")
    print(reg_patient)

    # -----------------------------------------------
    # Include microorganism/antimicrobial information
    # -----------------------------------------------
    # Libraries
    from pyamr.datasets.registries import MicroorganismRegistry
    from pyamr.datasets.registries import AntimicrobialRegistry

    # Load registry
    mreg = MicroorganismRegistry()
    areg = AntimicrobialRegistry()

    # Create genus and species
    reg_microorganism[['genus', 'species']] = \
        reg_microorganism.microorganism_name \
            .str.capitalize() \
            .str.split(expand=True, n=1)

    # Combine with registry information
    reg_microorganism = mreg.combine(reg_microorganism)
    reg_antimicrobial = areg.combine(reg_antimicrobial)

    # This fix with others in registries
    reg_antimicrobial.antimicrobial_name = \
        reg_antimicrobial.antimicrobial_name.str.lower()

    # Fill missing gram stain
    reg_microorganism.gram_stain = reg_microorganism.gram_stain.fillna('u')

    # -------------------------------------------------
    # Complete susceptibility records
    # -------------------------------------------------
    # Helper methods
    def drop_y(df):
        to_drop = [x for x in df if x.endswith('_y')]
        return df.drop(to_drop, axis=1)

    def rename_x(df):
        to_rename = {c: c.rstrip('_x')
            for c in df.columns if c.endswith('_x')}
        return df.rename(columns=to_rename)

    # Merge
    data = data.merge(reg_sensitivity,
        how='left', on='sensitivity_name')
    data = data.merge(reg_method,
        how='left', on='method_code')
    data = data.merge(reg_specimen,
        how='left', on=['specimen_code', 'specimen_description'])
    data = data.merge(reg_patient,
        how='left', on='patient_hos_number')
    data = data.merge(reg_microorganism[['microorganism_name',
                                         'microorganism_id']],
        how='left', on='microorganism_name')
    data = data.merge(reg_antimicrobial[['antimicrobial_name',
                                         'antimicrobial_id']],
        how='left', on='antimicrobial_name')

    # Drop and rename
    data = drop_y(data)
    data = rename_x(data)

    print(data)
    print(data.count())


    # -----------------------------------
    # Save to MySQL
    # ----------------------------------
    # Libraries
    from sqlalchemy import create_engine

    # Constants
    user = 'root'
    pwd = 'toor'
    host = 'localhost'
    schema = 'epicimpoc-test'
    fmt = 'mysql+pymysql://{user}:{pwd}@{host}/{schema}'

    # Create connection
    db_connection = create_engine(fmt.format(user=user,
        pwd=pwd, host=host, schema=schema))

    # Columns to keep
    keep = ['date_created', 'date_updated', 'date_received', 'date_outcome',
            'laboratory_number', 'mic', 'reported', 'antimicrobial_id',
            'method_id', 'microorganism_id', 'patient_id', 'sensitivity_id',
            'specimen_id']

    # Susceptibility tests
    aux = data.copy(deep=True)
    aux['date_created'] = pd.to_datetime('today')
    aux['date_updated'] = pd.to_datetime('today')
    aux = aux[keep]

    # Save
    aux.to_sql(name='microbiology_susceptibilitytest',
               con=db_connection,
               if_exists='replace',
               index=False)

    print(aux)

    import sys
    sys.exit()

    def sql_prepare_lookup(df):
        """Helper method to prepare lookup tables"""
        aux = df.copy(deep=True)
        # Remove prefixes
        aux.columns = [c.split('_', 1)[-1] for c in aux.columns]
        # Add missing columns
        aux['date_created'] = pd.to_datetime('today')
        aux['date_updated'] = pd.to_datetime('today')
        if not 'description' in aux:
            aux['description'] = ''
        if not 'is_visible' in aux:
            aux['is_visible'] = True
        # Fill na with '' so null=False.
        aux = aux.fillna(aux.dtypes.replace({'O': ''}))
        # Keep
        aux = aux[['id', 'name', 'code', 'description',
            'date_created', 'date_updated', 'is_visible']]
        aux = aux.drop_duplicates()
        # Return
        return aux

    LOOP = [#(reg_sensitivity, 'microbiology_sensitivity'),
            #(reg_specimen, 'microbiology_specimen'),
            (reg_method, 'microbiology_method'),
            #(reg_patient, 'microbiology_patient'),
            (reg_antimicrobial, 'microbiology_antimicrobial'),
            (reg_microorganism, 'microbiology_microorganism')]

    for df, name in LOOP:
        try:
            print("Importing.... %s" % name)
            sql_prepare_lookup(df) \
                .to_sql(name=name,
                    con=db_connection,
                    if_exists='append',
                    index=False)
        except Exception as e:
            print(e)



    import sys
    sys.exit()


    # -------------------------------------------------
    #
    # -------------------------------------------------
    # Specific
    from pathlib import Path

    # Time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Define path
    path = Path('./%s' % timestr)

    # Create path if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    # Save registries
    reg_patient.to_csv(path / 'patients.csv', index=False)
    reg_specimen.to_csv(path / 'specimens.csv', index=False)
    reg_sensitivity.to_csv(path / 'sensitivities.csv', index=False)
    reg_method.to_csv(path / 'methods.csv', index=False)
    reg_microorganism.to_csv(path / 'microorganisms.csv', index=False)
    reg_antimicrobial.to_csv(path / 'antimicrobial.csv', index=False)

    import sys
    sys.exit()

    # -------------------------------------------------
    # Create susceptibility test record from registries
    # -------------------------------------------------
    data = data.merge(reg_specimen['specimen_code'],
            how='left', left_on='specimen_code',
            right_on='specimen_code')

    data = data.merge(reg_sensitivity,
            how='left', left_on='sensitivity_name',
            right_on='sensitivity_name')

    data = data.merge(reg_method['method_code'],
            how='left', left_on='method_code',
            right_on='method_code')

    keep = ['date_received',
            'date_outcome',
            'laboratory_number',
            'specimen_id',
            'sensitivity_id',
            'method_id']

    # Show
    print(data[keep])