import pandas as pd

import sys
ANALYSIS_PATH = '/Users/idan/src/analysis_utils'
sys.path.append(ANALYSIS_PATH)

from confusion_matrix import ConfusionMatrix

def classifiy_commits_df(df
                         , classification_column
                         , classification_function):

    df[classification_column] = df.message.map(lambda x: classification_function(x) > 0)

    return df

def evaluate_performance(df
                         , classification_column
                         , concept_column):
    g = df.groupby(
        [classification_column, concept_column]
        , as_index=False).agg({'commit' : 'count'})
    cm = ConfusionMatrix(g_df=g
                                  ,classifier=classification_column
                                  ,concept=concept_column
                                  ,count='commit')

    return cm.summarize()

def evaluate_regex_results(labels_file
                           , classification_column
                           , classification_function
                           , concept_column
                           ):
    df = pd.read_csv(labels_file
                     , engine='python')
    df = classifiy_commits_df(df
                                , classification_column
                                , classification_function
                              )
    df.to_csv(labels_file
              , index=False)

    return evaluate_performance(df
                         , classification_column
                         , concept_column)


def evaluate_regex_results_on_df(df
                           , classification_column
                           , classification_function
                           , concept_column
                           ):
    df = classifiy_commits_df(df
                                , classification_column
                                , classification_function
                              )

    return evaluate_performance(df
                         , classification_column
                         , concept_column)