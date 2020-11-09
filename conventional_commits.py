# Conventional Commits 1.0.0
# https://www.conventionalcommits.org/en/v1.0.0/#specification

import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq
from model_evaluation import classifiy_commits_df, evaluate_performance

cc_adaptive_terms = ['feat', 'build', 'chore', 'ci', 'test']
cc_corrective_terms = ['fix']
cc_perfective_terms = ['docs', 'style', 'perf'] # TODO is perf -> perfective?
cc_refactor_terms = ['refactor']

cc_actions = cc_adaptive_terms + cc_corrective_terms + cc_perfective_terms + cc_perfective_terms

cc_etc = ['breaking\s+change(!)?:']


def cc_title(astions):

    return '^(' + "|".join(astions) +")(\(.*\))?(!)?:"


# Adaptive
def build_cc_adaptive_regex():

    return cc_title(cc_adaptive_terms)


def is_cc_adaptive(commit_text):

    return len(re.findall(build_cc_adaptive_regex(), commit_text)) > 0


# Corrective
def build_cc_corrective_regex():

    return cc_title(cc_corrective_terms)


def is_cc_corrective(commit_text):

    return len(re.findall(build_cc_corrective_regex(), commit_text)) > 0

# Refactor
def build_cc_refactor_regex():

    return cc_title(cc_refactor_terms)


def is_cc_refactor(commit_text):

    return len(re.findall(build_cc_refactor_regex(), commit_text)) > 0

# Just Perfective
def build_cc_just_perfective_regex():

    return cc_title(cc_perfective_terms)


def is_cc_just_perfective(commit_text):

    return len(re.findall(build_cc_just_perfective_regex(), commit_text)) > 0

# Perfective
def build_cc_perfective_regex():

    return "(" + "|".join([build_cc_refactor_regex()
                              , build_cc_just_perfective_regex()]) + ")"


def is_cc_perfective(commit_text):

    return len(re.findall(build_cc_perfective_regex(), commit_text)) > 0

# CC message
def build_cc_message_regex():

    return "(" + "|".join([cc_title(cc_actions)] + cc_etc) + ")"



def is_cc_message(commit_text):

    return len(re.findall(build_cc_message_regex(), commit_text)) > 0




def print_cc_functions_for_bq(commit: str = 'XXX'):

    concepts = {'cc_adaptive' : build_cc_adaptive_regex
                , 'cc_corrective' : build_cc_corrective_regex
                , 'cc_refactor' : build_cc_refactor_regex
                , 'cc_just_perfective' : build_cc_just_perfective_regex
                , 'cc_perfective' : build_cc_perfective_regex
                , 'cc_message' : build_cc_message_regex
                }

    for i in concepts.keys():
        print()
        print_func = lambda : print_logic_to_bq(regex_func=concepts[i]
                                                , concept=i)
        generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                            , concept=i)
                             , print_func
                             , commit=commit)
        print()


def evaluate_cc_fix_classifier():
    text_name = 'message'
    classification_function = is_cc_corrective
    classification_column = 'corrective_pred'

    concept_column = 'Is_Corrective'

    df = pd.read_csv(join(DATA_PATH, 'conventional_commits.csv'))


    df = classifiy_commits_df(df
                              , classification_function=classification_function
                              , classification_column=classification_column
                              , text_name=text_name
                              )
    cm = evaluate_performance(df
                              , classification_column
                              , concept_column
                              , text_name=text_name)
    print("corrective_labels CM")
    print(cm)

if __name__ == '__main__':
    print_cc_functions_for_bq()
    evaluate_cc_fix_classifier()
