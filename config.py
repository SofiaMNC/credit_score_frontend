
API_URL = "http://api_server:8080/v2/"

personal_info_cols = {
    'AMT_INCOME_TOTAL': "Income",
    'CNT_CHILDREN': "Children",
    'CNT_FAM_MEMBERS': "Family members",   
    'CODE_GENDER': "Gender",
    'DAYS_BIRTH': "Age",
    'DAYS_EMPLOYED': "Days at current job",
    'NAME_CONTRACT_TYPE': "Type of loan",
    'NAME_EDUCATION_TYPE': "Highest education",
    'NAME_FAMILY_STATUS': "Family status",
    'NAME_HOUSING_TYPE': "Housing situation",
    'NAME_INCOME_TYPE': "Income type",
    'NAME_TYPE_SUITE': "Accompanied by",
    'OCCUPATION_TYPE': "Occupation",
    'ORGANIZATION_TYPE': "Organization type" 
}

most_important_features_days = [
    'DAYS_EMPLOYED',
    'DAYS_BIRTH',
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