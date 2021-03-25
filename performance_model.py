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

excluded_terms = ['performance suite(?:s)?',
                  'performance (testing|test|tests)',
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
    print_concepts_functions_for_bq(commit='e524cdc5442d82628ce945d5a08befab9a52117b')
    #evaluate_performance_classifier()

    text = """
"ARM: EXYNOS4: Support early wakeup entering sleep mode

Since early wakeup can be handled in pm so we don't need masking
interrupts of external GIC. When the early wakeup interrupt happens,
PMU(Power Management Unit) ignores WFI instruction. This means that
PC(Program Counter) passed without any changes. This patch can handle
that case by early wakeup interrupt.

Signed-off-by: Jaecheol Lee <6ec43deacef8beeed37dec16d72a9fb9c16a0752@samsung.com>
[3fc711f4e08bc570a586748633ff7c76d0e1e253@samsung.com: fixed return of exynos4_cpu_suspend()]
Signed-off-by: Kukjin Kim <3fc711f4e08bc570a586748633ff7c76d0e1e253@samsung.com>
"
""".lower()
    print("is performance", is_performance(text))
    print("performance in text", re.findall(build_positive_regex(), text))


