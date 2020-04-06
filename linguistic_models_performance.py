import pandas as pd

from configuration import DATA_PATH
from confusion_matrix import ConfusionMatrix
from commit_type_model import classifiy_commits_df

def evaluate_bq_results(labels_file):
    df = pd.read_csv(labels_file
                     , engine='python')
    l = df[df.Type.isin(['corrective', 'perfective', 'adaptive', 'multi'])]

    l['corrective_pred'] = l['bq_classification']


    l['is_refactor_pred'] = l.refactor_matches.map(lambda x: x > 0)

    l['adaptive_pred'] = l.adaptive_matches.map(lambda x: x > 0)
    linguistic_model_perfomance(l)

def evaluate_regex_results(labels_file
                           , just_corrective=False):
    df = pd.read_csv(labels_file
                     , engine='python')
    df = classifiy_commits_df(df)
    linguistic_model_perfomance(df
                                , just_corrective=just_corrective)
    df.to_csv(labels_file
              , index=False)

def corrective_performance(df):
    bug_g = df.groupby(['corrective_pred', 'Is_Corrective'], as_index=False).agg({'commit' : 'count'})
    bug_cm = ConfusionMatrix(g_df=bug_g, classifier='corrective_pred', concept='Is_Corrective', count='commit')
    print( "corrective commit performance")
    print( bug_cm.summarize())

    return bug_cm

def refactor_performance(df):
    refactor_g = df.groupby(['is_refactor_pred', 'Is_Refactor'], as_index=False).agg({'commit' : 'count'})
    refactor_cm = ConfusionMatrix(g_df=refactor_g,classifier='is_refactor_pred',concept='Is_Refactor',count='commit')
    print( "refactor commit performance")
    print( refactor_cm.summarize())

    return refactor_cm

def adaptive_performance(df):
    adaptive_g = df.groupby(['adaptive_pred', 'Is_Adaptive'], as_index=False).agg({'commit' : 'count'})
    adaptive_cm = ConfusionMatrix(g_df=adaptive_g,classifier='adaptive_pred',concept='Is_Adaptive',count='commit')
    print( "adaptive commit performance")
    print( adaptive_cm.summarize())

    return adaptive_cm

def linguistic_model_perfomance(df
                                , just_corrective=False):

    corrective_performance(df)
    if not just_corrective:
        refactor_performance(df)
        adaptive_performance(df)


def get_false_positives(df
                        , classifier
                        , concept):
    return df[(df[classifier] == True) & (df[concept] == False)]

def get_false_negatives(df
                        , classifier
                        , concept):
    return df[(df[classifier] == False) & (df[concept] == True)]


def main():
    print( "test performance")
    print( "***********************************")
    evaluate_regex_results(DATA_PATH + 'repo2018_test.csv')
    #evaluate_bq_results(DATA_PATH + '/labels/commits_updated2.csv')

    print( "validation performance")
    print( "***********************************")
    evaluate_regex_results(DATA_PATH + 'model_validation_samples.csv'
                           , just_corrective=True)


if __name__ == '__main__':
    main()