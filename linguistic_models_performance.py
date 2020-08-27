import pandas as pd

from configuration import DATA_PATH
from confusion_matrix import ConfusionMatrix

from language_utils import match
from adaptive_model import is_adaptive
from corrective_model import is_fix
from refactor_model import built_is_refactor, build_perfective_regex, build_refactor_regex

def classifiy_commits_df(df):
    df['corrective_pred'] = df.message.map(lambda x: is_fix(x))
    df['is_refactor_pred'] = df.message.map(lambda x: built_is_refactor(x))
    df['perfective_pred'] = df.message.map(lambda x: (match(x, build_perfective_regex())) +
                                                     (match(x, build_refactor_regex())) > 0)
    df['adaptive_pred'] = df.message.map(lambda x: is_adaptive(x) > 0)

    return df


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