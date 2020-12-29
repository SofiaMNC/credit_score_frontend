
API_URL = "http://creditscoring-backend.herokuapp.com/v2/"

personal_info_cols = {
    'AMT_INCOME_TOTAL': "INCOME",
    'CNT_CHILDREN': "CHILDREN",
    'CNT_FAM_MEMBERS': "FAMILY MEMBERS",   
    'CODE_GENDER': "GENDER",
    'DAYS_BIRTH': "AGE",
    'DAYS_EMPLOYED': "YEARS AT CURRENT JOB",
    'NAME_CONTRACT_TYPE': "LOAN TYPE",
    'NAME_EDUCATION_TYPE': "HIGHEST EDUCATION",
    'NAME_FAMILY_STATUS': "FAMILY STATUS",
    'NAME_HOUSING_TYPE': "HOUSING SITUATION",
    'NAME_INCOME_TYPE': "INCOME TYPE",
    'NAME_TYPE_SUITE': "ACCOMPANIED BY",
    'OCCUPATION_TYPE': "OCCUPATION",
    'ORGANIZATION_TYPE': "ORGANIZATION TYPE" 
}

most_important_features_days = [
    'YEARS AT CURRENT JOB',
    'AGE',
]

most_important_features_amt = [
    'AMT_ANNUITY',
    'AMT_CREDIT'
]

most_important_features_ext = [
    'EXT_SOURCE_3',
    'EXT_SOURCE_2',
    'EXT_SOURCE_1'
]