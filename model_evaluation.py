import pandas as pd
from typing import Callable

import sys
ANALYSIS_PATH = '/Users/idan/src/analysis_utils'
sys.path.append(ANALYSIS_PATH)

from confusion_matrix import ConfusionMatrix

def classifiy_commits_df(df
                         , classification_column
                         , classification_function
                         , text_name: str ='message'):

    df[classification_column] = df[text_name].map(lambda x: classification_function(x) > 0)

    return df

def evaluate_performance(df
                         , classification_column
                         , concept_column
                         , text_name: str ='message'):
    g = df.groupby(
        [classification_column, concept_column]
        , as_index=False).agg({text_name : 'count'})
    cm = ConfusionMatrix(g_df=g
                                  ,classifier=classification_column
                                  ,concept=concept_column
                                  ,count=text_name)

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


def evaluate_regex_results_on_df(df: pd.DataFrame
                           , classification_column: str
                           , classification_function: Callable
                           , concept_column: str
                           , text_name: str ='message'
                           ):

    df = classifiy_commits_df(df
                                , classification_column
                                , classification_function
                                , text_name=text_name
                              )

    return evaluate_performance(df
                         , classification_column
                         , concept_column
                         , text_name=text_name)