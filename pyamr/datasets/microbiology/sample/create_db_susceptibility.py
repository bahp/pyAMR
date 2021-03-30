# Read
import glob
import pandas as pd


# ---------------------------------------
# Methods
# ---------------------------------------
def anonymise(series):
    """Basic anonymiser.

    Parameters
    ----------
    series: pd.Series
        The series with the patient ids.

    Return
    ------

    """
    # Create the replace map
    replace = dict(zip(series.unique(), range(series.nunique())))

    #replace = {i: name for i, name in enumerate(series.unique())}

    # Replace data
    transform = series.replace(replace)

    # Return
    return transform, replace




def clean_clwsql008(filepath):
    """This method cleans microbiology data from clwsql008.

    Full explanation of the steps of this method.

    .. notes: CLW-SQL-008
      - The sensitivity values found are
        { 'SS', 'R', 'ND', 'I', 'HIDE', 'HR' }

    .. note: Using UTC=True gives an error when using
             django-import-export to impot the data in
             the databases (commented).

    Parameters
    ----------
    filepath :

    Returns
    -------
    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # This dtype is important, specially for the
    # patient_nhs_number that otherwise will give
    # some problems (number poor visualisation).
    dtype = {
        'patient_nhs_number': object # it does not exist but PtNumber does.
    }

    rename = {
        'DiagnosticTestID': 'uuid',
        'PtNumber': 'patient_id',
        'AccNumber': 'laboratory_number',
        'BatTstCode': 'specimen_code',
        'OrderName': 'specimen_name',
        'SpecType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'OrgCode': 'microorganism_code',
        'Organism': 'microorganism_name',
        'DrugCode': 'antimicrobial_code',
        'AntiBiotic Name': 'antimicrobial_name',
        'SensMethod': 'sensitivity_method',
        'Sensitivity': 'sensitivity_code',
        'MIC': 'mic',
        'Reported': 'reported',
    }

    sensitivity_map = {
        'SS': 'sensitive',
        'R': 'resistant',
        'I': 'intermediate',
        'ND': 'not determined',
        'HR': 'highly resistant',
        'HIDE': 'hide'
    }

    # Load all files
    data = pd.concat([ \
        pd.read_csv(f, parse_dates={
            'date_received': ['ReceiveDate', 'ReceiveTime'],
            'date_outcome':['FinalDate']})
        for f in glob.glob(path + "/*.csv")])

    # Ignore those without result
    # df = df[~pd.isnull(df.result)]

    # Ignore those without hos number
    # .. note: Some of this rows might be valid. (receive_date?)
    # df = df[~pd.isnull(df.date_collection)]

    # Ignore those were the date of the result is null
    # .. note: Probably useless since all have it.
    # df = df[~pd.isnull(df.date_outcome)]

    # Format name and surname
    # df.patient_name = df.patient_name.str.title()
    # df.patient_surname = df.patient_surname.str.title()

    # --------------------------
    # Sensitivity
    # --------------------------
    # The sensitivity codes are given but the sensitivity names
    # are not included. We could use this opportunity to set
    # their values.
    # Step I: rename Sensitivity to sensitivity_code
    # Step II: add sensitivity_name with a manual mapping

    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values

    # Drop duplicates
    data.drop_duplicates(inplace=True)

    # Rename
    data = data.rename(columns=rename)
    data = data.convert_dtypes()
    data['sensitivity'] = data.sensitivity_code \
        .replace(sensitivity_map)

    # Show information
    print("\nFinal size: {0}".format(str(data.shape)))
    print("\nDtypes:")
    print(data.dtypes)
    print("\nNunique:")
    print(data.nunique())
    print("\nSensitivity: {0}".format( \
        list(data.sensitivity.unique())))

    #print(df.specimen_code.unique())
    #print(df.specimen_name.unique())
    #print(df.specimen_description.unique())

    # Return
    return data



# ---------------------------------------
# Constants
# ---------------------------------------

# ---------------------------------------
# Load data
# ---------------------------------------
# Define path
path = './raw'

# Create susceptibility data
susceptibility = clean_clwsql008(path)

# Get anonymised series
#anonymised, patient_map = anonymise(susceptibility.patient_id)

# Anonymise
#anonymised, replace = anonymise(susceptibility.patient_id)

print("\nData:")
print(susceptibility)



# Save
susceptibility.to_csv('susceptibility_v0.1.csv')