# Libraries
import pandas as pd

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
ANTIMICROBIAL_CODE_MAP = {
    'AAUGU': 'AAUG'
}

MICROORGANISM_CODE_MAP = {
    'ACINE2': 'ACINE',
    'CNS2': 'CNS',
    'CNS3': 'CNS',
    'ECOL2': 'ECOL',
    'KPN2': 'KPNE',
    'PAER2': 'PAER',
    'SAUR2': 'SAUR',
    'LFC2': 'LFC',
    'COLIF2': 'COLIF',
    'COLI2': 'COLIF',
    'ENTAE2': 'EAER',
    'ENTAE': 'EAER',
    'VRE': 'ENTC',
    'MRSA': 'SAUR',
    'MCNS': 'CNS',
    'A_ECOLI': 'ECOL',
    'A_ENTEROBA': 'ENTB',
    'A_SVIRIDANS': 'VIRST',
    'A_CLUSITANI': 'CLUS',
    'A_CDUBLINIE': 'CDUB',
    'A_CPSEUDODI': 'CPSEU'


}

SENSITIVITY_MAP = {
    'S': 'sensitive',
    'SS': 'sensitive',
    'R': 'resistant',
    'I': 'intermediate',
    'ND': 'not done',
    'HR': 'highly resistant',
    'HIDE': 'hide',
    '<<DO NOT REPORT>>': 'hide',
    '<<do not report>>': 'hide',
    'VALIDATION FIX ENTRY': 'fix',
    'validation fix entry': 'fix'
}

ANTIMICROBIAL_NAME_MAP = {
    '\([^)]*\)': '',  # Remove everything between ()
    '\s{2,}': ' ',  # Remove duplicated spaces
    'gentamicin 200': 'gentamicin'
}

MICROORGANISM_NAME_MAP = {
    # Replace basic
    'strep\.': 'streptococcus ',
    'staph\.': 'staphylococcus ',
    'species': 'sp.',
    'sp.($| )': '',
    'sp($| )': '',
    'second': '',
    'third': '',
    '2nd': '',
    '3rd': '',
    #'mixed': '',
    # Remove resistance
    'methicillin resistant': '',
    'vancomycin resistant': '',
    # Fix haemolytic hyphens
    'beta haemolytic': 'beta-haemolytic',
    'alpha haemolytic': 'alpha-haemolytic',
    'non haemolytic': 'non-haemolytic',
    # Revert genus name
    'beta-haemolytic streptococcus': 'streptococcus beta-haemolytic',
    'alpha-haemolytic streptococcus': 'streptococcus alpha-haemolytic',
    'non-haemolytic streptococcus': 'streptococcus non-haemolytic',
    'coagulase negative staphylococcus': 'staphylococcus coagulase negative',
    'lactose fermenting coliform': 'coliform lactose fermenting',
    'viridans streptococcus': 'streptococcus viridans',
    'milleri streptococcus': 'streptococcus milleri',
    'carboxyphilic streptococcus': 'streptococcus carboxyphilic',
    'microaerophilic streptococcus': 'streptococcus microaerophilic',
    # Specific
    '\*\*\* mrsa \*\*\* isolated': 'staphylococcus aureus',
    'escherichia coli o157': 'escherichia coli',
    'non - haemolytic streptococcus': 'streptococcus non-haemolytic',
    'mixed coagulase negative staphylococci': 'staphylococcus coagulase negative',
    'streptococcus milleri group': 'streptococcus milleri',
    'beta - haemolytic streptococcus not a - g': 'streptococcus beta-haemolytic group not A-G',
    'mixed alpha haemolytic streptococcus': 'streptococcus alpha-haemolytic mixed',
    'mixed anaerobes': 'anaerobes mixed',
    'beta-haemolytic streptococcus': 'streptococcus beta-haemolytic',
    'non-haemolytic streptococcus': 'streptococcus non-haemolytic',
    # 'beta-haemolytic streptococcus group a': 'streptococcus beta-haemolytic group A',
    # 'beta-haemolytic streptococcus group b': 'streptococcus beta-haemolytic group B',
    # 'beta-haemolytic streptococcus group c': 'streptococcus beta-haemolytic group c',
    # 'beta-haemolytic streptococcus group c/g': 'streptococcus beta-haemolytic group C/G',
    # 'beta-haemolytic streptococcus group g': 'streptococcus beta-haemolytic group G',
    # 'beta-haemolytic streptococcus group d': 'streptococcus beta-haemolytic group D',
    # 'beta-haemolytic streptococcus group f': 'streptococcus beta-haemolytic group F',
    #'beta - haemolytic streptococcus not a - g': 'streptococcus beta-haemolytic group not A-G',
    # Generic
    '\([^)]*\)': '',  # Remove everything between ()
    '\s{2,}': ' ',  # Remove duplicated spaces
}




def string_replace(series, remove={}):
    """This method corrects the strings.

    Parameters
    ----------

    Returns
    -------
    """
    # Format (lower)
    series = series.str.lower()
    # Do str replacements
    for k, v in remove.items():
        series = series.str.replace(k, v)
    # Format (strip)
    series = series.str.strip()
    # Return
    return series


def clean_clwsql008(data):
    """This method cleans microbiology data from clwsql008.

    Full explanation of the steps of this method.

    .. notes: CLW-SQL-008
      - The sensitivity values found are
        { 'SS', 'R', 'ND', 'I', 'HIDE', 'HR' }

    .. note: Using UTC=True gives an error when using
             django-import-export to import the data in
             the databases (commented).

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe with the data

    Returns
    -------
    pd.DataFrame
        The cleaned dataframe.
    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
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

    # Replace
    replace = {
        'sensitivity': SENSITIVITY_MAP,
        'microorganism_code': MICROORGANISM_CODE_MAP,
        'microorganism_name': MICROORGANISM_NAME_MAP,
        'antimicrobial_code': ANTIMICROBIAL_CODE_MAP
    }


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
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values

    # Drop duplicates
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    data = data.convert_dtypes()

    # Format strings
    data.antimicrobial_name = \
        string_replace(data.antimicrobial_name, ANTIMICROBIAL_NAME_MAP)
    data.microorganism_name = \
        string_replace(data.microorganism_name, MICROORGANISM_NAME_MAP)

    # Add columns (will be replaced later)
    if 'sensitivity_code' in data:
        data['sensitivity'] = data.sensitivity_code

    # Replacements
    data = data.replace(replace)

    # Format columns
    data.sensitivity = data.sensitivity.str.lower()

    # Drop duplicates
    data = data.drop_duplicates()

    #
    #data['date_received'] = pd.to_datetime(
    #    data['ReceiveDate'] + ' ' +  data['ReceiveTime'], errors='coerce')

    data['date_received'] = pd.to_datetime(
        data['date_received_date'] + ' ' +  data['date_received_time'], errors='coerce')

    data['date_outcome'] = pd.to_datetime(data['FinalDate'], errors='coerce')

    # Return
    return data



def clean_legacy(data):
    """This method cleans microbiology data from legacy.

    Full explanation of the steps of this method.

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe with the data

    Returns
    -------
    pd.DataFrame
        The cleaned dataframe.

    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'DiagnosticTestID': 'uuid',
        'patNumber': 'patient_id',
        'labNumber': 'laboratory_number',
        'orderCode': 'specimen_code',
        'orderName': 'specimen_name',
        'specimenType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'organismCode': 'microorganism_code',
        'organismName': 'microorganism_name',
        'antibioticCode': 'antimicrobial_code',
        'antibioticName': 'antimicrobial_name',
        'dateReceived': 'date_received'
    }

    # Replace
    replace = {
        'sensitivity': SENSITIVITY_MAP,
        'microorganism_code': MICROORGANISM_CODE_MAP,
        'microorganism_name': MICROORGANISM_NAME_MAP,
        'antimicrobial_code': ANTIMICROBIAL_CODE_MAP,
        'antimicrobial_name': ANTIMICROBIAL_NAME_MAP
    }

    # Ignore those without sensitivity outcome
    data = data[data.sensitivity.notna()]

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
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values

    # Drop duplicates
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    data = data.convert_dtypes()

    # Format strings
    data.antimicrobial_name = \
        string_replace(data.antimicrobial_name, ANTIMICROBIAL_NAME_MAP)
    data.microorganism_name = \
        string_replace(data.microorganism_name, MICROORGANISM_NAME_MAP)

    # Add columns (will be replaced later)
    #data['sensitivity'] = data.sensitivity_code

    # Replacements (they should be all done from raw! a the moment it depends on the corrector sHIT!
    data = data.replace(replace)

    # Format columns
    data.sensitivity = data.sensitivity.str.lower()


    data.loc[data.microorganism_name == 'arcanobacterium haemolyticum', 'microorganism_code'] = 'A_ARCANOHAEMO'
    data.loc[data.microorganism_name == 'acinetobacter haemolyticum', 'microorganism_code'] = 'A_ACINETOHAEMO'

    # --------------------
    # Cleaning dates
    # --------------------
    # Clean date received
    if 'date_received' in data:
        # Convert to datetime.
        data.date_received = \
            pd.to_datetime(data.date_received, errors='coerce')

        # Remove rows with required columns missing
        #data = data.dropna()

        # Ignore those without result
        data = data[data.sensitivity.notna()]

        # Ignore those without hos number
        data = data[data.date_received.notna()]



    # Drop duplicates
    data = data.drop_duplicates()

    # Return
    return data


def clean_mimic(data):
    """This method...

    .. note: Need to merge datetime for date and datetime for time
             as done in the datablend package if want full info.

    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'subject_id': 'patient_id',
        'micro_specimen_id': 'laboratory_number',
        'spec_type_desc': 'specimen_description',
        'test_seq': 'microorganism_piece_counter',
        'org_name': 'microorganism_name',
        'ab_name': 'antimicrobial_name',
        'test_name' : 'sensitivity_method',
        'interpretation': 'sensitivity',
        'chartdate': 'date_received',
        'storedate': 'date_ouctome'
    }

    # Replace values
    replace = {
        'sensitivity': SENSITIVITY_MAP,
        'microorganism_code': MICROORGANISM_CODE_MAP,
        'microorganism_name': MICROORGANISM_NAME_MAP,
        'antimicrobial_code': ANTIMICROBIAL_CODE_MAP
    }

    # Rename
    data = data.rename(columns=rename)

    # Replace
    data = data.replace(replace)

    # Format
    data.microorganism_name = data.microorganism_name.str.capitalize()
    data.antimicrobial_name = data.antimicrobial_name.str.capitalize()
    data['microorganism_code'] = data.microorganism_name
    data['antimicrobial_code'] = data.antimicrobial_name
    data['specimen_code'] = data.specimen_description

    # Format date
    if 'date_received' in data:

        # Convert to datetime.
        data.date_received = \
            pd.to_datetime(data.date_received, errors='coerce')

        # Ignore those without result
        data = data[data.sensitivity.notna()]

    # Return
    return data