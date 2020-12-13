import pandas as pd

def get_filtered_client_data(app_data, filter_dict, tolerance=0.1):
    '''
        Get filtered data according to criteria
    '''

    criteria = [k for k,v in filter_dict.items() if str(v) != "*"]
    
    # Create dictionary with key = criterium and value = dataframe filtered on criterium
    criteria_dfs = []

    for criterium in criteria:
        value = filter_dict[criterium]

        if criterium in ["DAYS_BIRTH", "AMT_INCOME_TOTAL"]:
            if criterium == "DAYS_BIRTH":
                lowest_value = value + value*tolerance
                highest_value = value - value*tolerance
            else:
                lowest_value = value - value*tolerance
                highest_value = value + value*tolerance

            criteria_dfs.append(app_data[(app_data[criterium] >= lowest_value)
                                         &
                                         (app_data[criterium] <= highest_value)])
        else:
            criteria_dfs.append(app_data[app_data[criterium] == value])

    # Result dataframe keeping only the rows satisfying all conditions
    results_df = pd.DataFrame()

    if not criteria:
        results_df = app_data
    else:
        results_df = criteria_dfs[0]

    for i in range(1, len(criteria_dfs)):    
        results_df = pd.merge(left=results_df, right=criteria_dfs[i][["SK_ID_CURR"]], 
                              left_on='SK_ID_CURR', right_on='SK_ID_CURR')

    return results_df
