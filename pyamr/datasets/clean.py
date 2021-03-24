# Libraries
import pandas as pd

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
microorganism_gram_type = {
    'SAUR': 'p',
    'AHS': 'p',
    'BCER': 'p',
    'BACIL': 'p',
    'BHSA': 'p',
    'BHSB': 'p',
    'BHSC': 'p',
    'BHSCG': 'p',
    'BCEP': 'n',
    'BPSE': 'n',
    'CCOL': 'n',
    'CFET': 'n',
    'CJEJ': 'n',
    'CAMPY': 'n',
    'CPER': 'p',
    'CLOST': 'p',
    'CNS': 'p',
    'CHAE': 'p',
    'CJEI': 'p',
    'CORYN': 'p',
    'CSTR': 'p',
    'ENTAE'	:'n',
    'EASB'	:'n',
    'ECLO'	:'n',
    'ENTB'	:'n',
    'ECASS' :'p',
    'EFAS'  :'p',
    'EFAM'	:'p',
    'EGAL'	:'p',
    'ENTC'	:'p',
    'ECOL'	:'n',
    'FNEC'	:'n',
    'KOXY'	:'n',
    'KPNE'	:'n',
    'KLEBS'	:'n',
    'LMON'	:'p',
    'SAUR'	:'p',
    'NFLA'	:'n',
    'NGON'  :'n',
    'NMEN'  :'n',
    'NEISS'	:'n',
    'NHS'	:'p',
    'PANA'	:'p',
    'PACN'	:'p',
    'PROPI'	:'p',
    'PMIR'	:'n',
    'PROTE'	:'n',
    'PVUL'	:'n',
    'PSEUD'	:'n',
    'PAER'	:'n',
    'PLUT'	:'n',
    'PORI'	:'n',
    'PPUT':'n',
    'PSTU':'n',
    'SALMO':'n',
    'SLIQ':	'n',
    'SMAR':	'n',
    'SERRA':'n',
    'SFLE':	'n',
    'SSON':	'n',
    'SHIGE':'n',
    'SEPI':	'p',
    'SHAEM':'p',
    'SLUG':	'p',
    'SSAP':	'p',
    'STAPH':'p',
    'SAGA':	'p',
    'SANG':	'p',
    'SCON':	'p',
    'SDYSEQ':'p',
    'SEQU':	'p',
    'SGOR':	'p',
    'SINT':	'p',
    'SMIL':	'p',
    'SMIT':	'p',
    'SORA':	'p',
    'SPARAS':'p',
    'SPNE':	'p',
    'SPYO':	'p',
    'SSAL':	'p',
    'SSAN':	'p',
    'STREP': 'p',
    'ENTC': 'p',
    'YENT':	'n'
}

antimicrobial_class = {
    'AAMPC': None,
    'AAMI':	'aminoglycosides',
    'AAMO':	'aminopenicillins',
    'AAMPH': None,
    'AAND': None,
    'AAUG': None,
    'AAZI':	'macrolides',
    'AAZT':	'monobactams',
    'ABAC':	'polypeptides',
    'ACPO': None,
    'ACAS': None,
    'ACIX':	'cephalosporins',
    'ACTX':	'cephalosporins',
    'ACXT':	'cephalosporins',
    'ACAZ':	'cephalosporins',
    'ACONE': 'cephalosporins',
    'ACXM': 'cephalosporins',
    'ACELX': 'cephalosporins',
    'ACHL': None,
    'ACIP':	'fluoroquinolones',
    'ACLA':	'macrolides',
    'ACLI':	'macrolides',
    'ACOL':	'polypeptides',
    'ACOT':	'sulfonamides',
    'ADAP': None,
    'AERT':	'meropenems',
    'AESBL': None,
    'AERY':	'macrolides',
    'AMET':	'penicillins',
    'AFLUZ': None,
    'AFLUC'	: None,
    'AFOS'	: None,
    'AFUS'	: None,
    'AGEN':	'aminoglycosides',
    'AGEN':	'aminoglycosides',
    'AIMP':	'meropenems',
    'AITR'	: None,
    'ALEV'	:'fluoroquinolones',
    'ALIN':	'oxazolidinones',
    'AMLS': None,
    'AMEC':	'penicillins',
    'AMER':	'meropenems',
    'AMTZ':	'nitroimidazoles',
    'AMF':  None,
    'AMOX':	'fluoroquinolones',
    'AMUP': None,
    'ANAL':	'fluoroquinolones',
    'ANEO':	'aminoglycosides',
    'ANIT': None,
    'ANOV':	'aminocoumarin',
    'AOFL':	'fluoroquinolones',
    'AOPT': None,
    'AOXA':	'penicillins',
    'APEF': None,
    'APEN':	'penicillins',
    'APCZ': None,
    'ARIF': None,
    'ASEP': None,
    'ASYN': None,
    'ATAZ': None,
    'ATEI':	'glycopeptide',
    'ATEM':	'penicillins',
    'ATET':	'tetracyclines',
    'ATIG':	'tetracyclines',
    'ATOB':	'aminoglycosides',
    'ATRI': None,
    'AVAN':	'glycopeptide',
    'AVOR': None}

def string_corrector(series, remove={}):
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

def gram_type_from_code():
    """This method.."""
    # Create dataframe
    df_gram = pd.DataFrame()
    df_gram['microorganism_code'] = gram_type.keys()
    df_gram['microorganism_gram_type'] = gram_type.values()
    # Return
    return df_gram

def antimicrobial_class_from_code():
    """This method..."""
    df = pd.DataFrame()
    df['antimicrobial_code'] = antimicrobial_class.keys()
    df['antimicrobial_class'] = antimicrobial_class.values()
    # Return
    return df


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

    microorganism_code_map = {
        'ACINE2': 'ACINE',
        'CNS2': 'CNS',
        'CNS3': 'CNS',
        'ECOL2': 'ECOL',
        'KPN2': 'KPNE',
        'PAER2': 'PAER',
        'SAUR2': 'SAUR',
        'VRE': 'ENTC',
        'MRSA': 'SAUR',
        'MCNS': 'CNS'
    }

    microorganism_name_map = {
        'viridans streptococcus': 'streptococcus viridans',
        'lactose fermenting coliform': 'coliform lactose fermenting',
        'coagulase negative staphylococcus': 'staphylococcus coagulase negative',
        'beta-haemolytic streptococcus group a': 'streptococcus beta-haemolytic group A',
        'beta-haemolytic streptococcus group b': 'streptococcus beta-haemolytic group B',
        'beta-haemolytic streptococcus group c/g': 'streptococcus beta-haemolytic group C/G',
        'mixed coagulase negative staphylococci': 'staphylococcus coagulase negative'
    }

    antimicrobial_code_map = {
        'AAUGU': 'AAUG'
    }

    replace = {
        'sensitivity': sensitivity_map,
        'microorganism_code': microorganism_code_map,
        'microorganism_name': microorganism_name_map,
        'antimicrobial_code': antimicrobial_code_map
    }

    antimicrobial_name_remove = {
        '\([^)]*\)': '',  # Remove everything between ()
        '\s{2,}': ' ',    # Remove duplicated spaces
    }

    microorganism_name_remove = {
        'sp.': '',
        'sp': '',  # order matters
        'second': '',
        'third': '',
        '2nd': '',
        '3rd': '',
        'methicillin resistant': '',
        'vancomycin resistant': '',
        '\([^)]*\)': '', # Remove everything between ()
        '\s{2,}': ' ',   # Remove duplicated spaces
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
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    data = data.convert_dtypes()

    # Format strings
    data.antimicrobial_name = \
        string_corrector(data.antimicrobial_name, antimicrobial_name_remove)
    data.microorganism_name = \
        string_corrector(data.microorganism_name, microorganism_name_remove)

    # Add columns (will be replaced later)
    data['sensitivity'] = data.sensitivity_code

    # Replacements
    data = data.replace(replace)

    # Drop duplicates
    data = data.drop_duplicates()

    # Return
    return data
