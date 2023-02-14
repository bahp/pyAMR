# Libraries






if __name__ == '__main__':

    # Libraries generic
    import time
    import glob
    import pandas as pd

    # Libraries specific
    from pyamr.datasets.clean import clean_basic
    from pyamr.datasets.clean import clean_clwsql008
    from pyamr.datasets.clean import clean_legacy

    # -------------------------------------------
    # Load data
    # -------------------------------------------
    # Define tuples
    tuples = [
        ('./nhs/clwsql008', clean_clwsql008),
        #('./nhs/legacy', clean_legacy),
        #('./nhs/test', clean_clwsql008),
        #('./nhs/test2', clean_legacy)
    ]

    # Combined data
    combined = []

    # For each tuple
    for path, f_clean in tuples:
        # Debug information
        print("Loading... {0}".format(path))
        # Load data (multiple files)
        data = pd.concat([pd.read_csv(f, #nrows=100,
            encoding="ISO-8859-1", engine='c')
                for f in glob.glob(path + "/*.csv")])
        # Clean data
        data = f_clean(data, clean_microorganism=True)
        # Combine
        combined.append(data)

    # Concatenate
    data = pd.concat(combined)

    # It was already within cleaners.
    data = clean_basic(data)

    # Show
    print("\nData:")
    print(data)
    print("\nColumns:")
    print(data.dtypes)


    # -------------------------------------------------
    # Quick and dirty for patient (improve)
    # -------------------------------------------------
    data = data.rename(columns=\
        {'patient_hos_number': 'patient_name'})

    # -------------------
    # Create registries
    # -------------------
    # Information
    print("Creating registries...")

    # Libraries
    from pyamr.datasets.registries import Registry
    from pyamr.datasets.registries import MicroorganismRegistry
    from pyamr.datasets.registries import AntimicrobialRegistry

    # Create registries
    regm = Registry(keyword='method', subset=None).fit(data)
    regx = Registry(keyword='specimen',
        subset=['name', 'code', 'description']).fit(data)
    regs = Registry(keyword='sensitivity').fit(data)
    regp = Registry(keyword='patient').fit(data)
    rego = MicroorganismRegistry(keyword='microorganism').fit(data)
    rega = AntimicrobialRegistry(keyword='antimicrobial').fit(data)

    # Show information
    print("\nSensitivity:")
    print(regs.getr())
    print("\nMethod:")
    print(regm.getr())
    print("\nSpecimen:")
    print(regx.getr())
    print("\nMicroorganism:")
    print(rego.getr())
    print("\nAntimicrobial:")
    print(rega.getr())
    print("\nPatient:")
    print(regp.getr())

    # -------------------------------------------------
    # Format susceptibility test records
    # -------------------------------------------------
    # Information
    print("Formatting susceptibility test records...")

    # Add all the ids
    for r in [regm, regx, regs, rego, rega, regp]:
        data['%s_id' % r.keyword] = \
            r.replace(data['%s_name' % r.keyword],
                key='name', value='id')

    # Why this is soooo slow!
    #for r in [regm, regx, regs, rego, rega, regp]:
    #    data = r.transform(data)


    # -------------------------------------------------
    # Save
    # -------------------------------------------------
    # Information
    print("Creating folder...")

    # Specific
    import csv
    from pathlib import Path

    # Time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Define path
    path = Path('./%s' % timestr)

    # Create path if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    # Save registries
    regx.getr().to_csv(path / 'specimen.csv', index=False)
    regs.getr().to_csv(path / 'sensitivity.csv', index=False)
    regm.getr().to_csv(path / 'method.csv', index=False)
    rego.getr().to_csv(path / 'microorganism.csv', index=False)
    rega.getr().to_csv(path / 'antimicrobial.csv', index=False)
    regp.getr().to_csv(path / 'patient.csv', index=False)

    # ----------
    # Filter
    # ----------
    # We have to remove those dates in which the date_received is none
    # because otherwise we cannot group the data by year to store it
    # in different files. In addition, the others are also required to
    # have a meaningful susceptibility test record.
    data = data.dropna(how='any',
                       subset=['date_received',
                               'specimen_code',
                               'microorganism_name',
                               'antimicrobial_name',
                               'sensitivity_name'])

    data = data.drop_duplicates()
    data = data.reset_index(drop=True)
    data['id'] = data.index + 1

    # ----------
    # Save
    # ----------
    # Columns
    keep = ['id',
            'date_received',
            'date_outcome',
            'patient_hos_number',
            'laboratory_number',
            'specimen_code',
            'specimen_name',
            'specimen_description',
            'microorganism_code',
            'microorganism_name',
            'antimicrobial_code',
            'antimicrobial_name',
            'method_code',
            'method_name',
            'sensitivity_code',
            'sensitivity_name',
            'mic',
            'reported',
            'microorganism_id',
            'antimicrobial_id',
            'sensitivity_id',
            'method_id',
            'specimen_id',
            'patient_id']

    # Filter
    data = data[[c for c in keep if c in data]]

    # Create grouper
    grouper = pd.Grouper(key='date_received', freq='Y')

    # .. note: To verify that the date_format do not check
    #          the excels since the format the dates to
    #          by yyy/mm/dd, instead check the raw csvs.

    # Save susceptibility grouped
    for n, g in data.groupby(grouper):
        # Create filename
        filename = "susceptibility-%s.csv" % n.strftime('%Y')
        # Save
        g.to_csv(path / filename, index=False,
                 date_format='%Y-%m-%d %H:%M:%S',
                 quoting=csv.QUOTE_ALL)  # QUOTE_NONNUMERIC

    # Logging
    #logger.info('The results have been saved in: %s' % path)



    import sys
    sys.exit()











    # --------------------------------------------
    # Create registries
    # --------------------------------------------
    # Library
    from pyamr.datasets.registries import create_registry
    
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