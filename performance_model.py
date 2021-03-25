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

excluded_terms = ['performance suite(?:s)?',
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
    print_concepts_functions_for_bq(commit='52a7c8257bcf835e778750bd5c5f172a5cba281f')
    #evaluate_performance_classifier()

    text = """
"drm/i915: Kill intel_crtc->cursor_bo

The vma may have been rebound between the last time the cursor was
enabled and now, so skipping the cursor gtt offset deduction is not
safe unless we would also reset cursor_bo to NULL when disabling the
cursor. Just thow cursor_bo to the bin instead since it's lost all
other uses thanks to universal plane support.

Chris pointed out that cursor updates are currently too slow
via universal planes that micro optimizations like these wouldn't
even help.

v2: Add a note about futility of micro optimizations (Chris)

Cc: 2dacef862dfeb083b5f3bcc5c29009f436dd5241@lists.freedesktop.org
References: http://lists.freedesktop.org/archives/intel-gfx/2015-December/082976.html
Cc: Chris Wilson <711c73f64afdce07b7e38039a96d2224209e9a6c@chris-wilson.co.uk>
Cc: Takashi Iwai <4596b3305151c7ee743192a95d394341e3d3b644@suse.de>
Cc: Jani Nikula <ba783f3beccaedfda693f41a15407d612a629408@linux.intel.com>
Signed-off-by: Ville Syrjälä <cd6e8d405ca90be3a03d5427c5b24fbd2d68dcc4@linux.intel.com>
Link: http://patchwork.freedesktop.org/patch/msgid/1450107302-17171-1-git-send-email-cd6e8d405ca90be3a03d5427c5b24fbd2d68dcc4@linux.intel.com
Reviewed-by: Chris Wilson <711c73f64afdce07b7e38039a96d2224209e9a6c@chris-wilson.co.uk>
(cherry picked from commit 1264859d648c4bdc9f0a098efbff90cbf462a075)
Signed-off-by: Jani Nikula <ba783f3beccaedfda693f41a15407d612a629408@intel.com>
"
""".lower()
    print("is performance", is_performance(text))
    print("performance in text", re.findall(build_positive_regex(), text))


