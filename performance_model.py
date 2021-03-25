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
    #'(cpu|gpu|tpu)',
    #'day(?:s)?',
    '(fast|faster|fastest)',
    #'hour(?:s)?',
    'improv' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    '(long|longer|short|shorter|above|least)' + NEAR_ENOUGH + 'time(?:s)?',
    #'minute(?:s)?',
    'optimiz' + VERB_E_SUFFIX,
    'optimization',
    'performance',
    'reduc' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    #'second(?:s)?',
    '(speed|speeding)',
    'tak' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    #'run(?: |-)?time(?:s)?',
    '(slow|slower|slowest)',
    ]

excluded_terms = ['[a-z0-9/\.]*fast/[a-z0-9/\.]*',
                  'performance suite(?:s)?',
                  'performance (testing|test|tests)',
                  'sometime(?:s)?',
                  '(unnoticed|found)' + NEAR_ENOUGH + 'long time',
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
    print_concepts_functions_for_bq(commit='b933d243b0cb403f21d467e72a6362d143cd18ef')
    #evaluate_performance_classifier()

    text = """
"Calculate client positions from offsets.
https://bugs.webkit.org/show_bug.cgi?id=73640

Reviewed by Tony Chang.

This change calculates client positions from offset positions at run time to
remove platform-dependent constants from this test.

* fast/events/offsetX-offsetY-expected.txt:
* fast/events/offsetX-offsetY.html:
* platform/chromium-win/fast/events/offsetX-offsetY-expected.txt: Removed.


git-svn-id: bf5cd6ccde378db821296732a091cfbcf5285fbd@121735 bbb929c8-8fbe-4397-9dbb-9b2b20218538"
""".lower()
    print("is performance", is_performance(text))
    print("performance in text", re.findall(build_positive_regex(), text))


