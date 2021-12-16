"""
A model for identifying Self Admitted Technical Debt (SATD)
"""

import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH, term_seperator
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier


# Using the list from
# An exploratory study on self-admitted technical debt by Potdar, Aniket and Shihab, Emad
positive_terms = ['fixme', 'hack', 'todo', 'xxx']

removal_terms = [
    'because'
    , 'clean' + REGULAR_SUFFIX
    , 'fix' + REGULAR_SUFFIX
    , 'implement' + REGULAR_SUFFIX
    , 'list' + REGULAR_SUFFIX
    , 'remov' + VERB_E_SUFFIX
    , 'was'
]
excluded_terms = ['update TODO(\.)?'
    , "(%s)%s(%s)/" % ("|".join(removal_terms), NEAR_ENOUGH, "|".join(positive_terms))
    , "(%s)/" % ("|".join(positive_terms))
    , '\.xxx'
    , '=xxx'
                  ]

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_satd(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def satd_to_bq():
    concept = 'satd'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_satd(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_satd(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_satd(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):


    concepts = {'core_satd' : build_positive_regex
        , 'excluded_satd': build_excluded_regex
        , 'not_positive_satd' : build_not_positive_regex
        #, 'satd': satd_to_bq

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

    generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                        , concept='satd')
                         , satd_to_bq
                         , commit=commit)
    print()
def evaluate_satd_classifier():

    evaluate_concept_classifier(concept='satd'
                                , text_name='message'
                                , classification_function=is_satd
                                , samples_file=join(DATA_PATH, 'satd_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='4ed9f7272f45a3dd6c4dd7f04fe3ab77f633ab10')
    evaluate_satd_classifier()

    text = """TODO\n""".lower()
    print("Label", is_satd(text))
    print("concept in text", re.findall(build_positive_regex(), text))
