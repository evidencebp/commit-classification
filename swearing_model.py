# TODO https://www.rypeapp.com/blog/english-swear-words/
# TODO https://en.wiktionary.org/wiki/Category:English_swear_words
# TODO https://www.joe.co.uk/life/a-definitive-ranking-of-every-swear-word-from-worst-to-best-122544

import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

# Not sure list
"""
'disappointing|disheartening|displeasing|mortifying|not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|scary|shameful|shame|shocking|repulsive|revolting|stink'
#, 'poor'
"""

positive_terms =['awful',
 'crap',
 'disgusting',
 'fuck(en|ing|s|ed)?',
 'hideous',
 'horrible',
 'lousy',
 'mortifying',
 'repulsive',
 'revolting',
 'rotten',
 'shameful',
 'shit',
 'stink(s|ing|ed)?',
 'terrible']

excluded_terms = ['awful\.[a-z]' # Name of a common component
                  ]

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_swearing(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def swearing_to_bq():
    concept = 'swearing'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_swearing(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_swearing(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_swearing(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):


    concepts = {'core_swearing' : build_positive_regex
        , 'excluded_swearing': build_excluded_regex
        , 'not_positive_swearing' : build_not_positive_regex
        #, 'swearing': swearing_to_bq

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
                                                        , concept='swearing')
                         , swearing_to_bq
                         , commit=commit)
    print()
def evaluate_swearing_classifier():

    evaluate_concept_classifier(concept='Is_swearing'
                                , text_name='message'
                                , classification_function=is_swearing
                                , samples_file=join(DATA_PATH, 'swearing_hits_dataset.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='fedd454d2bf47de43b2bc80d52172ab8aac33bc7')
    evaluate_swearing_classifier()

