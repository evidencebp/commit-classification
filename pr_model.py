

import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, software_goals, software_entities
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

thinking = ['think', 'know', 'thought']
we_terms = ['we', 'our']
you_terms = ['you', 'your', 'u']
politness = ['should', 'would', 'might', 'may', 'please', 'thanks', 'sorry']
suggestion = ['can', 'do']
# TODO add negation
# TODO - add questions
order = ['need', 'sure', 'needs', 'never']
discussion = ['but', 'actually', 'why', 'reason', 'check', 'maybe', 'because', 'question', 'since', 'discussed'
    , 'explain', 'clarify', 'answer', 'understanding'
              ]
observation = ['seems', 'looks', 'guess', 'probably', 'believe', 'wonder', 'sounds', 'suppose', 'wondering', 'looking'
               , 'says']

positive_approach = ['agree', 'understand', 'prefer', 'suggest', 'feel', 'tried', 'forgot', 'assume', 'found', 'agree'
                     , 'disagree' # ?
                     , 'feels', 'realize', 'love', 'confused', 'suspect', 'suggestion', 'curious', 'happy'
                     , 'suggested', 'seen', 'realized', 'appreciate'
                     ]

negative = ['fair', 'rid', 'hate', 'weird', 'odd', 'strange']
negative_approach = ['missed', 'avoid', 'overlooked', 'surprised', 'afraid', 'doubt', 'worried', 'concerned']
alternatives = ['instead'
                , 'used' # ?
                ]
# mean, meant
# must
# point
#very
# sense
#correct
#exactly
# wrong
# least
# consistency


formatting_terms = ['double(?:-|\s)quoted string(?:s)?', 'format', 'space(?:s)?', 'spacing', 'tab(?:s)?','white(?:-|\s)?space(?:s)?'
, 'trailing', 'more than one line', 'align', 'line(?:s)?', 'indentation', 'brace(?:s)?', '{', '}', '\(', '\)', '\[', '\]'
, 'multi(?:-|\s)?line', 'new(?:-|\s)?line(?:s)?', 'align(s|ed|ing|ment)', 'ident(s|ed|ing)?', 'parentheses'
, 'line is too long', 'colon(?:s)?', 'quote(?:s|d)?', 'fqcn', 'vendor prefix(?:s)?', 'semi(?:-|\s)?colon(?:s)?'
, 'format(?:ing)?']

formatting_excluded_terms = []

code = ['private', 'public', 'const', 'final', 'static', 'inline']
# __[rails_best_practices]__
# avoid, allowed, should have



def build_formatting_regex():

    return build_sepereted_term(formatting_terms)

def build_software_goals_regex():

    return build_sepereted_term(software_goals)

def build_software_entities_regex():

    return build_sepereted_term(software_entities)

def build_formatting_excluded_regex():

    return build_sepereted_term(formatting_excluded_terms)

def build_not_formatting_regex():

    return build_non_positive_linguistic(build_formatting_regex())


def is_good(commit_text):

    return (len(re.findall(build_formatting_regex(), commit_text))
            - len(re.findall(build_formatting_excluded_regex(), commit_text))
            - len(re.findall(build_not_formatting_regex(), commit_text)))  > 0



def good_to_bq():
    concept = 'formatting'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_formatting(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_formatting(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_formatting(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concepts = {'core_formatting' : build_formatting_regex
        , 'excluded_formatting': build_formatting_excluded_regex
        , 'not_positive_formatting' : build_not_formatting_regex
        , 'core_build_software_goals' : build_software_goals_regex
        , 'core_build_software_entities' : build_software_entities_regex
        #, 'good': good_to_bq

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
                                                        , concept='good')
                         , good_to_bq
                         , commit=commit)
    print()

if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='a942729125a8b28078af5ab49296e395dd05fb0d')
