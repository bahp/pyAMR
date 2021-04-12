# Libraries
import numpy as np
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

SPECIMEN_CODE_MAP = {
    'URNCUL': 'URICUL'
}

SPECIMEN_NAME_MAP = {
    'Urine Micro': 'Urine Culture'
    
}
# '9MRSN': 'MRSCUL',
# 'URINE CULTURE': 'URICUL',
# 'WOUND CULTURE': 'WOUCUL',
# 'BLOOD CULTURE': 'BLDCUL',
# 'SPUTUM CULTURE': 'SPTCUL',
##'CSF CULTURE': 'CSFCUL',
# 'EYE CULTURE': 'EYECUL',
# 'GENITALCUL': 'GENCUL',
# 'NEONATAL SCREEN': 'NEOCUL',

METHOD_CODE_MAP = {
    'DD': 'Disk Difussion',
    'PHO': 'PHO',
    'MIC': 'Minimum Inhibitory Concentration',
    'MASTU': 'MASTU',
}

SENSITIVITY_CODE_MAP = {
    'S': 'sensitive',
    'SS': 'sensitive',
    'R': 'resistant',
    'I': 'intermediate',
    'ND': 'not done',
    'HR': 'highly resistant',
    'HIDE': 'hide',
    '<<DO NOT REPORT>>': 'hide',
    'VALIDATION FIX ENTRY': 'fix',
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


def clean_common(data):
    """This method...

    Parameters
    ----------

    Returns
    -------
    """
    # ------------------------------
    # Missing columns and replace
    # ------------------------------
    # All uppercase first
    #data = data.apply(lambda x: x.astype(str).str.upper())
    #data = data.replace('nan', value=np.nan)

    # We should be able to generalise this to all, but remember
    # that it is important to keep the NaN and not have an string
    # representation 'nan'.
    # Format title
    for c in ['sensitivity_code',
              'sensitivity_name',
              'method_code',
              'method_name']:
        if c in data:
            data[c] = data[c].str.upper()

    # Add method name if it does not exist
    if not 'method_name' in data:
        if 'method_code' in data:
            data['method_name'] = data.method_code

    # Add sensitivity name if it does not exist
    if not 'sensitivity_name' in data:
        if 'sensitivity_code' in data:
            data['senstivity_name'] = data.sensitivity_code

    # Replace
    data = data.replace({
        'method_name': METHOD_CODE_MAP,
        'sensitivity_name': SENSITIVITY_CODE_MAP,
    })

    # ------------------------------
    # String formatting
    # ------------------------------
    # Format title
    for c in ['patient_name',
              'patient_surname']:
        if c in data:
            data[c] = data[c].str.title()

    # Format lower
    for c in ['antimicrobial_name',
              'microorganism_name',
              'sensitivity_name',
              'method_name']:
        if c in data:
            data[c] = data[c].str.lower()

    # Format upper
    for c in ['antimicrobial_code',
              'microorganism_code',
              'sensitivity_code',
              'method_code']:
        if c in data:
            data[c] = data[c].str.upper()

    # ------------------------------
    # Time formatting
    # ------------------------------
    # Format date-times
    for c in ['date_received', 'date_outcome']:
        if c in data:
            data[c] = pd.to_datetime(data[c], errors='coerce')

    # We could also use the convert_dtypes, however there is a big
    # issue with the pd.NA values. I think that issue is only if
    # we want to apply replace and there are pd.NA (only works with
    # np.nan) but it should be fine now that all that has been done.
    #data = data.convert_dtypes()

    # Remove empty (sensitivity, date_received, ...?)
    #data = data.dropna(how='any', subset=[])

    # Drop duplicates
    data = data.drop_duplicates()

    # Return
    return data


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
        'ReceiveDate': 'received_date',
        'ReceiveTime': 'received_time',
        'PtNumber': 'patient_hos_number',
        'AccNumber': 'laboratory_number',
        'BatTstCode': 'specimen_code',
        'OrderName': 'specimen_name',
        'SpecType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'OrgCode': 'microorganism_code',
        'Organism': 'microorganism_name',
        'DrugCode': 'antimicrobial_code',
        'AntiBiotic Name': 'antimicrobial_name',
        'SensMethod': 'method_code',
        'Sensitivity': 'sensitivity_name',
        'MIC': 'mic',
        'Reported': 'reported',
        'FinalDate': 'date_outcome'
    }

    # Replace
    replace = {
        #'sensitivity': SENSITIVITY_MAP,
        'microorganism_code': MICROORGANISM_CODE_MAP,
        'microorganism_name': MICROORGANISM_NAME_MAP,
        'antimicrobial_code': ANTIMICROBIAL_CODE_MAP
    }

    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values
    # Drop duplicates
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    #data = data.convert_dtypes()

    # Format strings
    data.antimicrobial_name = \
        string_replace(data.antimicrobial_name, ANTIMICROBIAL_NAME_MAP)
    data.microorganism_name = \
        string_replace(data.microorganism_name, MICROORGANISM_NAME_MAP)

    # Add columns (will be replaced later)
    #data['sensitivity_name'] = data.sensitivity_code \
    #    .str.upper().replace(SENSITIVITY_CODE_MAP)
    #    #.str.upper().map(SENSITIVITY_CODE_NAME_MAP) # Map leaves nulls

    # Replacements
    data = data.replace(replace)

    # Set new columns
    data['date_received'] = pd.to_datetime(
        data.received_date + ' ' + data.received_time, errors='coerce')

    # Final formatting
    data = clean_common(data)

    # Return
    return data



def clean_legacy(data):
    """This method cleans microbiology data from legacy.

    Full explanation of the steps of this method.
    1. Rename the columns to align with standard.
    2. Apply replace using common maps.
    3. Apply common formatting.

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
        'dateReceived': 'date_received',
        'age': 'age',
        'gender': 'gender',
        'patNumber': 'patient_hos_number',
        'labNumber': 'laboratory_number',
        'orderCode': 'specimen_code',
        'orderName': 'specimen_name',
        'specimenType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'organismCode': 'microorganism_code',
        'organismName': 'microorganism_name',
        'antibioticCode': 'antimicrobial_code',
        'antibioticName': 'antimicrobial_name',
        'sensitivity': 'sensitivity_name'
    }

    # Replace
    replace = {
        #'sensitivity': SENSITIVITY_MAP,
        'microorganism_code': MICROORGANISM_CODE_MAP,
        'microorganism_name': MICROORGANISM_NAME_MAP,
        'antimicrobial_code': ANTIMICROBIAL_CODE_MAP,
        'antimicrobial_name': ANTIMICROBIAL_NAME_MAP
    }

    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values
    # Drop duplicates
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    #data = data.convert_dtypes() # issue with np.nan in replace
    #data = data[data.sensitivity.notna()] # no sensitivity


    # Format strings
    data.antimicrobial_name = \
        string_replace(data.antimicrobial_name, ANTIMICROBIAL_NAME_MAP)
    data.microorganism_name = \
        string_replace(data.microorganism_name, MICROORGANISM_NAME_MAP)

    # Add columns (will be replaced later)
    #data['sensitivity'] = data.sensitivity_code

    # Replacements (they should be all done from raw! a the moment it depends on the corrector sHIT!
    data = data.replace(replace)

    #data.loc[data.microorganism_name == 'arcanobacterium haemolyticum', 'microorganism_code'] = 'A_ARCANOHAEMO'
    #data.loc[data.microorganism_name == 'acinetobacter haemolyticum', 'microorganism_code'] = 'A_ACINETOHAEMO'

    # Final formatting
    data = clean_common(data)

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
        'subject_id': 'patient_hos_number',
        'micro_specimen_id': 'laboratory_number',
        'spec_type_desc': 'specimen_description',
        'test_seq': 'microorganism_piece_counter',
        'org_name': 'microorganism_name',
        'ab_name': 'antimicrobial_name',
        'test_name' : 'method',
        'interpretation': 'sensitivity_name',
        'chartdate': 'date_received',
        'storedate': 'date_outcome'
    }

    # Replace values
    replace = {
        #'sensitivity': SENSITIVITY_MAP,
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