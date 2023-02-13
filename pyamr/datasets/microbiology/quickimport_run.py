# Libraries generic
import pandas as pd
from pathlib import Path

def quickimport(path, connection):
    """


    :param path:
    :param connection:
    :return:
    """
    # -----------------------------------------------
    # Import lookup tables
    # -----------------------------------------------
    # Information
    print("Importing lookup tables...")

    # Lookup tables
    lookup = ['sensitivity.csv',
              'method.csv',
              'specimen.csv',
              'antimicrobial.csv',
              'microorganism.csv']

    keep = ['id', 'date_created', 'date_updated',
            'name', 'code', 'description', 'is_visible']

    for lp in lookup:
        # Read DataFrame
        df = pd.read_csv('%s/%s' % (path, lp))

        # Rename columns (remove in the future)
        #df.columns = [c.split("_")[-1] for c in df.columns]

        # Add dates
        df['date_created'] = pd.to_datetime('today')
        df['date_updated'] = pd.to_datetime('today')

        # Add missing
        if not 'description' in df:
            df['description'] = None
        if not 'is_visible' in df:
            df['is_visible'] = True

        # Fill na with '' so null=False.
        df = df.fillna(df.dtypes.replace({'O': ''}))

        # Keep
        df = df[keep]

        # Keep columns
        #print(df.name.value_counts())

        # Save
        try:
            df.to_sql(name='microbiology_%s' % Path(lp).stem,
                  con=connection,
                  #if_exists='replace',
                  if_exists='append',
                  index=False)
        except Exception as e:
            print(e)


    # ------------------------------------------------
    # Import patient
    # ------------------------------------------------
    df = pd.read_csv('%s/%s' % (path, 'patient.csv'))
    # Add dates
    df['date_created'] = pd.to_datetime('today')
    df['date_updated'] = pd.to_datetime('today')
    # Fill na with '' so null=False.
    df = df.fillna(df.dtypes.replace({'O': ''}))
    # Keep
    df = df.rename(columns={'name': 'hos_number'})
    df['name'] = ''
    df['surname'] = ''
    df['gender'] = 'M'
    df = df[['hos_number', 'id', 'date_created', 'date_updated', 'name',
             'surname', 'gender']]

    # Save
    try:
        df.to_sql(name='microbiology_%s' % 'patient',
                  con=connection,
                  # if_exists='replace',
                  chunksize=None,
                  if_exists='append',
                  index=False)
    except Exception as e:
        print(e)

    # ------------------------------------------------
    # Import data
    # ------------------------------------------------
    # Information
    print("Importing susceptibility tests...")

    # Load data
    data = pd.concat([pd.read_csv(f, #nrows=1000,
        encoding="ISO-8859-1", engine='c')
            for f in glob.glob(path + "/susceptibility-*.csv")])

    # Add missing
    data['date_created'] = pd.to_datetime('today')
    data['date_updated'] = pd.to_datetime('today')

    # Columns to keep
    keep = ['id',
            'date_created', 'date_updated', 'date_received', 'date_outcome',
            'laboratory_number',  'reported', 'antimicrobial_id',
            'method_id', 'microorganism_id', 'patient_id', 'sensitivity_id',
            'specimen_id'] #'mic',

    data = data[keep]

    # Save
    data.to_sql(name='microbiology_susceptibilitytest',
               con=connection,
               if_exists='append',
               index=False)




if __name__ == '__main__':

    # Libraries generic
    import glob
    import pandas as pd

    # Libraries specific
    from sqlalchemy import create_engine

    # Path
    path = './20210423-132035'

    # Connection parameters
    user = 'root'
    pwd = 'toor'
    host = 'localhost'
    schema = 'epicimpoc'
    fmt = 'mysql+pymysql://{user}:{pwd}@{host}/{schema}'

    # Create connection
    connection = create_engine(fmt.format(user=user,
        pwd=pwd, host=host, schema=schema))

    # Run quick import
    quickimport(path=path, connection=connection)