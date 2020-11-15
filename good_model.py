"""
Building a local shallow syntax based language model.

If the positive ratio is expected to be high enough classify some texts.
That will give the ability to estimate the positive rate, recall and improve the model's recall.
In many cases, the positive rate is very low and therefore this method is not applicable.

Guess some terms related to the concept. Brainstorms are helpful.
Look for synonyms of the terms.
https://www.thesaurus.com/

Look of common tokens in text contaning your terms.

Sort the terms by alphabetical order to group them by semantic meaning.
It will be valuable in maintaining.

Sample some hits containing the terms.
Browse them, see that you are OK and fine tune them.

Add build_non_positive_linguistic,
# TODO - others?

Add a list of supersets of your terms to be excluded

Samples hits of core that are not hits of your model to improve model recall

Tests
Archimedes

Term evaluation

Maintain a list of cases that you are not ceartin about. Time helps.
"""


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

# Not sure list
"""
superior,  first-string
"""
improvement = ['better', 'improved', 'fitter', 'preferred', 'finer', 'greater'
, 'higher quality'
]

positive_terms =['A number 1',
 'acumen',
 'admirable',
 'adored',
 'amazing',
 'astonishing',
 'astounding',
 'awesome',
 'beautiful',
 'best',
 'best ever',
 'best-quality',
 'breathtaking',
 'brilliance',
 'brilliant',
 'charming',
 'clever',
 'cool',
 'cute',
 'dandy',
 'delightful',
 'dignified',
 'elegant',
 'excellent',
 'exceptional',
 'extraordinary',
 'fabulous',
 'fantastic',
 'fine',
 'finest',
 'first-class',
 'first-rate',
 'five-star',
 'flawless',
 'genius',
 'good',
 'gorgeous',
 'great',
 'greatest',
 'high-caliber',
 'highest-quality',
 'honorable',
 'impressive',
 'incredible',
 'ingenious',
 'ingenuity',
 'lovely',
 'magnific',
 'magnificent',
 'marvelous',
 'neat',
 'nice',
 'notable',
 'ok',
 'outstanding',
 'perfect',
 'phenomenal',
 'pleasing',
 'praiseworthy',
 'precious',
 'premium',
 'pretty',
 'remarkable',
 'respectable',
 'shipshape',
 'smart',
 'spectacular',
 'splendid',
 'splendid',
 'state-of-the-art',
 'stunning',
 'super',
 'super-duper',
 'super-eminent',
 'super-excellent',
 'superb',
 'superior',
 'supreme',
 'terrific',
 'tip-top',
 'top of the line',
 'top-notch',
 'ultimate',
 'valuable',
 'well-made',
 'well-thought-of',
 'wise',
 'wonderful',
 'world-class']

excluded_terms = ['for good', 'good way', 'good news', 'great time']

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def is_good(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text)))  > 0



def good_to_bq():
    concept = 'good'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_good(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_good(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)


def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concepts = {'core_good' : build_positive_regex
        , 'excluded_good': build_excluded_regex
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
def evaluate_good_classifier():

    evaluate_concept_classifier(concept='good'
                                , text_name='message'
                                , classification_function=is_good
                                , samples_file=join(DATA_PATH, 'good_texts_tests.csv'))


if __name__ == '__main__':
    #print_concepts_functions_for_bq(commit='XXX')
    evaluate_good_classifier()
