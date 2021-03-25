"""

"""


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, NEAR_ENOUGH, VERB_E_SUFFIX
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

# Not sure list
"""
"""

positive_terms = [
    'better' + NEAR_ENOUGH + 'time(?:s)?',
    '(cpu|gpu|tpu)',
    'day(?:s)?',
    'hour(?:s)?',
    'improv' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    '(long|longer|short|shorter|above|least)' + NEAR_ENOUGH + 'time(?:s)?',
    'minute(?:s)?',
    'optimiz' + VERB_E_SUFFIX,
    'optimization',
    'performance',
    'reduc' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    'second(?:s)?',
    '(speed|speeding)',
    'tak' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    'run(?: |-)?time(?:s)?',
    '(slow|slower|slowest)',
    ]

excluded_terms = ['performance suite(?:s)?',
                  ]

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_performance(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def performance_to_bq():
    concept = 'performance'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_{concept}(message)".format(schema=SCHEMA_NAME
                                                       , concept=concept))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_{concept}(message)".format(schema=SCHEMA_NAME
                                                           , concept=concept))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_{concept}(message)".format(schema=SCHEMA_NAME
                                                               , concept=concept))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concept = 'performance'

    concepts = {'core_' + concept : build_positive_regex
        , 'excluded_' + concept : build_excluded_regex
        , 'not_positive_' + concept : build_not_positive_regex
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
                                                        , concept=concept)
                         , performance_to_bq
                         , commit=commit)
    print()
def evaluate_performance_classifier():

    evaluate_concept_classifier(concept='performance'
                                , text_name='message'
                                , classification_function=is_performance
                                , samples_file=join(DATA_PATH, 'commit_performance_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='9795cc67ad63133d19686a96d965ae784fddaee7')
    #evaluate_performance_classifier()

    text = """
"Sensitivity plots fix (#2860)

* fix immediately obvious bug in plotting loop

* add in allinj plots, create front summary page

* move allinj to after injection plots loop

* Fix to make bank_plot work. Include found table in injection pages

* Use censored veto, clarify fixme comments

* add snrifar summary to main page

* remove confusing and unneccessary bit

* found table doesnt work

* fix up one thing which turned into a list although it's only a list with 1 entry

* add Gareth"
""".lower()
    print("is performance", is_performance(text))
    print("performance in text", re.findall(build_positive_regex(), text))


