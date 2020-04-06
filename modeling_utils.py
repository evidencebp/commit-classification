import pandas as pd

def compute_data_sets_distinctivnes(first_file
                                    , second_file
                                    , key='commit'):
    first_df = pd.read_csv(first_file
                           , engine='python')
    second_df = pd.read_csv(second_file
                            , engine='python')

    return len(first_df), len(second_df), len(first_df[first_df[key].isin(second_df[key])])
