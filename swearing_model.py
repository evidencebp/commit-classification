"""

Sources
# https://www.rypeapp.com/blog/english-swear-words/
# https://en.wiktionary.org/wiki/Category:English_swear_words
# https://www.joe.co.uk/life/a-definitive-ranking-of-every-swear-word-from-worst-to-best-122544
# https://www.cs.cmu.edu/~biglou/resources/bad-words.txt
# https://core.ac.uk/download/pdf/162166124.pdf

# https://twitter.com/gitlost # A twitter account that post developers swearing.
https://github.com/travisnelson/sneezymud/blob/20590efc5e0fbd6b9d9236e0d0591af5da600d4f/code/constants.cc
http://www.commitlogsfromlastnight.com/ # Suggested by thatguywiththatname2
"""


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

positive_terms =[
 'arse',
 'arsehole',
 'ass(?:es)?',
 'ass(?: |-)?hole(?:s)?',
 'awful',
 # 'bad', # In most cases not used as a swear in programming context
 'bastard(?:s)?',
 'bint',
 'bitch(?:e)?(?:s)?',
 'bloody',
 'bloody hell',
 'bloody oath',
 'bollocks',
 'bugger',
 'bullshit',
 'choad',
 'christ',
 'clunge',
 'cock',
 'crap',
 'cunt',
 'cow',
 'clusterfuck(?:s)?',
 'dammit',
 'damn',
 'damnit',
 'dick(?:s)?',
 'dick(?:-|\s)?head(?:s)?',
 'dirty',
 'disgusting',
 'dumb',
 'effing',
 'fanny',
 'fool(ish)?',
 '(fuck|f\*ck|f\*\*k)(er|en|ing|s|ed)?',
 'fucktard',
 '(father|mother|brother|sister|child)(?:-|\s)?(fuck|f\*ck|f\*\*k)er',
 'freak',
 'jfdi', # Just F do it
 'jesus',
 'hell',
 'hideous',
 'horseshit',
 'horrible',
 #'garbage', # Consider
 'gash',
 '(get|got) stuffed',
 #'git', # Aware of it, not suitable for git commit messages
 'goddamn',
 'godsdamn',
 'lousy',
 'lunatic',
 'lousy',
 'maniac',
 'moron',
 'mortifying',
 'nasty',
 'piss(ing|s|ed)',
 'piss(ing|s|ed)?(?:-|\s)?off',
 'poor',
 'prick',
 'punani',
 'punk',
 'pussy',
 'repulsive',
 'revolting',
 'rotten',
 'rtfm', # Read The F Manual
 'rubbish',
 'shag',
 'shame',
 'shameful',
 'shit',
 'shit(?:-|\s)?ass',
 'slap(?:s)? code',
 'slut(?:s)?',
 'snatch',
 'sod',
 'son of a bitch',
 'stink(s|ing|ed)?',
 'stupid',
 'suck(s|ing|ed)?',
 'taking (a|the) piss',
 'terrible',
 'tit(?:s)?',
 'trash',
 'twat(?:s)?',
 'ugl(y|ies|iest)',
 'wanker(?:s)?',
 'whore(?:s)?',
 'wtf',

 ]

excluded_terms = ['awful\.[a-z]*', # Name of a common component
                  'brainfuck', # Programming language
                  'clever as hell',
                  'garbage collect(e|es|ed|ing|ion)',
                  'nasty (bug|error)',
                  'my bad',
                  'not bad',
                  'shit happens',
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

    evaluate_concept_classifier(concept='Swearing'
                                , text_name='body'
                                , classification_function=is_swearing
                                , samples_file=join(DATA_PATH, 'pull_request_swearing_hits.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='fedd454d2bf47de43b2bc80d52172ab8aac33bc7')
    evaluate_swearing_classifier()

