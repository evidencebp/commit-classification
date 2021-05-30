import re

from conventional_commits import build_cc_refactor_regex
from language_utils import file_scheme, term_seperator, build_sepereted_term, negation_terms, modals\
    , regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, documentation_entities, prefective_entities\
    , software_terms, build_non_positive_linguistic, software_goals_modification, software_goals, static_analyzers

# TODO - add Technical Debt, fixme
"""
Directions to consider 

Spaghetti code - indication of mess, not always a refactor
Useless (as dead code)
"""

# https://arxiv.org/pdf/2002.11049.pdf
refactor_entities = software_terms + ['(helper|utility|auxiliary) function(?:s)?']


# Well, we need them...
unnedded_terms = ['unnecessary', 'unneeded', 'unused', '(?:not|never|no longer) used'
    #, 'old'
    , 'no longer needed', 'redundant', 'useless', 'duplicate(?:d)?', 'deprecated', 'obsolete(?:d)?', 'commented']

core_refactor_terms = [
    'clean(?:ing)?(?:-| )?up(?:s)?',
    'clean(?:ing|s|ed)?',
    'combin(?:e|es|ed|ing)',
    'compos(?:e|es|ed|ing)',
    'de(?:-| )?compos(?:e|es|ed|ing)',
    'deprecat(?:e|es|ed|ing)',
    'encapsulat(?:e|es|ed|ing)',
    'polish(?:ed|es|ing)?',
    're(?:-| )?factor(?:ed|s|ing|ings)?', # TODO - should be here - check why slightly decreases performance
    're(?:-|)?organiz(?:e|es|ed|ing)',
    're(?:-|)?structur(?:e|es|ed|ing)',
    'rebuil(?:d|ds|ding|t)',
    'tid(?:y|ying|ied)'
]


modification_activity = [
'(?:get|got|getting) rid',
 '(?:make|makes|made|making)',
 'convert(?:ed|s|ing)?',
 'dead',
 'drop(?:ed|s|ing)?',
 'duplicat(?:e|es|ed|ing)',
 'extract(?:ed|s|ing)?',
 'hide(?:e|es|ed|ing)',
 'improv(?:e|es|ed|ing)',    # Goals modification only?
 'increas(?:e|es|ed|ing)',
 'mov(?:e|es|ed|ing)',
 'parameteriz(?:e|es|ed|ing)',
 'redundant',
 'replac(?:e|es|ed|ing)',
 'separat(?:e|e s|ed|ing)',
 'short(:?en|er|ing|s)?',
 'split(?:s|ing)?',
 'subsitut(?:e|es|ed|ing)',
 'substitut(?:e|es|ed|ing)',
 'un(?:-| )?hid(?:e|es|ed|ing)'

    #'chang(?:e|esed|ing)'
    #, 'creat(?:e|es|ed|ing)'
    #, 'delet(?:e|es|ed|ing)'
    #, 'instead'
    #, 'kill(?:ed|s|ing)?'
    # , 'provid(?:e|es|ed|ing)'
    #, 'introduc(?:e|es|ed|ing)'
] + core_refactor_terms + unnedded_terms

feedbak_terms = [ 'py(?:-| )?lint', 'lint', 'review comments(?:s)?', 'code review', 'cr', 'pep8'
                  ]
feedback_action = ['fix(?:ed|s|es|ing)?', 'fix(?:-| )?up(?:s)?', 'resolv(?:e|ed|es|ing)', 'correct(?:ed|s|es|ing)?']

perfective_header_action = [
    #'polish(?:ed|es|ing)?'
    #, 'clean(?:ing|s|ed)?(?:-| )?up(?:s)?'
     'clean(?:ing|s|ed)?(?:-| )?up(?:s)?'
    , 'cleaner'
    , 'deprecat(?:e|es|ed|ing)'
    , 'extract(?:ed|s|ing)?',
    're(?:-|)?organiz(?:e|es|ed|ing)', 're(?:-|)?structur(?:e|es|ed|ing)', 'tid(?:y|ying|ied) up'
    , 'improv(?:e|ed|es|ing|ement|ements)' , 're(?:-|)?organiz(?:e|es|ed|ing)', 're(?:-|)?structur(?:e|es|ed|ing)'
    , '(helper|utility|auxiliary) function(?:s)?'
    , '(?:move|moved|moves|moving) to'
    , 'separat(?:e|es|ed|ing)'
    , 'split(?:s|ing)?', '->'
    , build_sepereted_term(static_analyzers) + 'fix(es|ed)?'
    , 'fix(es|ed)?' + build_sepereted_term(static_analyzers)

    #, '(private|public|protected|static)'
]

# TODO - rewrited, move into/out???, deduplicate, remove legacy, redo, PR, feedback

# TODO - clean , style, prettier, "->", refine, "Removed commented code", "More startup improvements.", recode
# ""Remove another old function", "improved redis error message", utility functions, never used
# Checkstyle


# TODO - perfective, not refactor - ident, spacing, tabs, "tabs -> spaces", cosmetic, ""*** empty log message ***"
# examples ""DOC: remove mention of TimeSeries in docs"

# TODO - add "resolving review comments"
# TODO - lint, pylint
refactor_context = [ 'clean(ing)?(-| )?up(s)?'
    ,'call(?:s|ed|ing)?[\s\S]{1,50}instead'
    , 'collaps(?:e|es|ed|ing)', 'consolidat(e|es|ed|ing)'
    , 'decompos(?:e|es|ed|ing)'
    , 'drop(?:ed|s|ing)?( back)', 'encapsulat(e|es|ed|ing)'
    , 'gereneliz(?:e|es|ed|ing)'
                    # , 'inline'
                    # , 'no longer needed', 'not used', 'obsolete(d)?'
    , 'optimiz(?:e|es|ed|ing|ation|ations)'
    , 'pull(?:ed|s|ing)? (up|down)', 're(?:-)?(?:write|wrote)', 're(?:-| )?factor(?:ed|s|ing|ings)?'
    , 're(-)?implement(ed|s|ing)?'
    , 'renam(?:e|es|ed|ing|ings)', 'better nam(?:e|es|ing)','re(?:-)?organiz(e|es|ed|ing)', 're(?:-)?organization'
    , 're(?:-)?work(ed|s|ing|ings)?'
    , 'reorg' , 'simplif(y|es|ied|ying|ication)', 'suppress(es|ed|ing)? warning(?:s)?'
    , 'unif(?:y|ies|ied|ing)', 'uninline'
    , 'beef(?:ed|s|ing)? up', 'refactor(?:ing)?(?:s)?', 'code improvement(?:s)?'
    #, '(?:^|^[\s\S]{0,25}%s)(?:%s)%s[\s\S]{0,25}$' % (term_seperator, "|".join(perfective_header_action), term_seperator)
    , 'revis(?:e|es|ed|ing)'
    , 're(?:-)?construct(?:s|ed|ing)?'
    , 're(?:-)?(?:write|write|wrote|writing)'
    , 're(?:-)?cod(?:e|ed|es|ing)'
    , 'factor(?:ed|s|ing)? out'
    , 're(?:-| )?packag(?:e|es|ed|ing)'
    #, 'code review'
    #, 'collapse'
    #, "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(feedback_action
    #                                                                                      , just_before=True)
    #                                                                 , term_seperator
    #                                                                 , term_seperator
    #                                                                 , term_seperator
    #                                                                 , "|".join(feedbak_terms)
    #                                                                 , term_seperator)
                    # ,'us(e|es|ed|ing)[\s\S]{1,50}(instead)'
                    # , '(instead)[\s\S]{1,50}us(e|es|ed|ing)'
                    ]
# https://refactoring.guru/refactoring/techniques

# TODO - change [\s\S] with . ?
removal = [ 'add(?:s|ed|ing)?[\s\S]{1,50}helper(?:s)?'
    ,  'us(?:e|es|ed|ing)[\s\S]{1,50}instead'
    #,  'us(?:e|es|ed|ing)[\s\S]{1,25}\(\)[\s\S]{1,25}instead'
    ,  'split(?:s|ing)?[\s\S]{1,50}into'
    ,  'break(?:s|ing)?[\s\S]{1,50}into'
    ,  'separat(?:e|e s|ed|ing)[\s\S]{1,50}into'
    #,  'replac(?:e|es|ed|ing)?[\s\S]{1,50}with'
    ,  'replac(?:e|es|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    , 'remov(?:e|es|ed|ing)[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    #, '(?:this|that|is)[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'kill(?:s|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'drop(?:s|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'mov(?:e|es|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
            ]
adaptive_context = [
    '(?:un)?hid(?:e|es|den)', 'add(?:s|ed|ing)?', 'allow(?:s|ed|ing)?'
    , 'buil(?:t|ds|ing)', 'calibirat(?:e|es|ed|ing)'
    , 'configure'
    , 'creat(?:e|es|ing)' #   O created
    , 'deferr(?:ed|s|ing)?'
    , 'disabl(?:e|es|ed|ing)'
    , 'enhanc(?:e|es|ed|ing)', 'extend(?:s|ed|ing)?', 'form(?:ed|s|ing)?'
    , 'implement(?:ed|s|ing)?', 'import(?:s|ed|ing)?', 'introduc(?:e|es|ed|ing)'
    , 'port(?:s|ed|ing)?'
    , 'provid(?:e|es|ed|ing)'
    , 'report(?:s|ed|ing)?'
    , 'support(s|ed|ing)?'
    , 'updat(?:e|es|ed|ing)'
    , 'upgrad(?:e|es|ed|ing)'

    # , 'mov(e|es|ed|ing)'
    # , 'print(s|ed|ing)?'


]

def build_core_refactor_regex():

    return '(%s)' % build_sepereted_term(core_refactor_terms)

def is_core_refactor(text):
    return match(text, build_core_refactor_regex())


def build_refactor_regex(use_conventional_commits=True):
    header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)%s' % (term_seperator
                                                       , "|".join(perfective_header_action)
                                                       , term_seperator)

    activity_regerx = "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(modification_activity
                                                                                          , just_before=True)
                                                                     , term_seperator
                                                                     , term_seperator
                                                                     , term_seperator
                                                                     , "|".join(refactor_entities)
                                                                     , term_seperator)
    if use_conventional_commits:
        agg_re = "(%s)|(%s)|(%s)|(%s)" % (build_sepereted_term(refactor_context)
                          , activity_regerx
                          , header_regex
                          , build_cc_refactor_regex())
    else:
        agg_re = "(%s)|(%s)|(%s)" % (build_sepereted_term(refactor_context)
                          , activity_regerx
                          , header_regex)
    return agg_re



def build_refactor_goals_regex():
    goals_regerx = "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(software_goals_modification
                                                                                       , just_before=True)
                                                                  , term_seperator
                                                                  , term_seperator
                                                                  , term_seperator
                                                                  , "|".join(software_goals)
                                                                  , term_seperator)
    return goals_regerx


def build_non_code_perfective_regex():

    non_perfective_entities = ['warning(?:s)?'
                               , 'format(?:ing)?'
                               , 'indentation(?:s)?'
                              ]
    # TODO - applied to perfective entities too here, which is a bug.
    modification_action = ['clean(?:-| )?up(?:s)?']
    non_perfective_context = [
                            'fix(?:es|ed|ing)?'
                            ,'(?:get|got|getting) rid'
                            , 'support(?:s|ed|ing)?'
                            ]
    modifiers = modification_activity + non_perfective_context
    activity_regerx = "((?:%s)(?:\s|%s[\s\S]{0,50}%s)(?:%s))" % (build_sepereted_term(modifiers, just_before=True)
                                                                                , term_seperator
                                                                                , term_seperator
                                                                                , "|".join(prefective_entities
                                                                                           + non_perfective_entities))
    doc_header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)[\s\S]{0,25}(?:%s)' % (term_seperator
                                                       , "|".join(perfective_header_action)
                                                       , build_sepereted_term(documentation_entities))


    no_prefective_action = "|".join([
        'convert(?:ed|s|ing)?(?:%s|%s[\s\S]{0,50}%s)support(?:s|ed|ing)?' % (
            term_seperator,term_seperator, term_seperator)
        , '(?:make|made|making|makes)(?:%s|%s[\s\S]{0,50}%s)work' % (term_seperator, term_seperator, term_seperator)
        , '(?:make|made|making|makes)(?:%s|%s[\s\S]{0,50}%s)sense' % (term_seperator, term_seperator, term_seperator)
        , 'improv(?:e|es|ed|ing) handling'
        , 'need(?:s|ing)?\srefactor(?:ing)?'
        , '(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)' %(build_sepereted_term(non_perfective_entities,just_before=True)
                                                   ,term_seperator
                                                   , term_seperator
                                                   , term_seperator
                                                   , "|".join(modification_action)
                                                   )
        , doc_header_regex

    ])
    non_perfective_context = '(?:%s|%s)' % (no_prefective_action
                                         , activity_regerx)

    return non_perfective_context


def build_documentation_entities_context(positive_re):

    return '(?:%s)' % "|".join([
        # TODO - take care of documentation entities spereatly
         '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(documentation_entities, just_before=True)
                                        ,positive_re)
    ])



# instead of
# make sure
# missed to create
# can be replaced, e9dee4fc76caaca231bf10728d4f82bc46581bc5
# no seperation for create eb1027b5e8c047059f68e7547188d08c7fde0b6f
# inline c9d4924dcf129512dadd22dcd6fe0046cbcded43
# can be optimized 197fc962fa8a3153dc058abfa2ae8c816d67ea04
# corrective trouble (use wordnet) b580f0706dc1dcded6d1a584c37a83dd1cb2ea2a
# not used 72894b26c24b1ea31c6dda4634cfde67e7dc3050


def core_refactor_to_bq():
    print("# Core Refactor Term")
    print( regex_to_big_query(build_core_refactor_regex()))
    print("#Core Refactor Term - end")

def positive_refactor_to_bq():
    print( "# Refactor :build_refactor_regex()")
    #print( ",")
    print( regex_to_big_query(build_refactor_regex()))
    print( "# Refactor :build_sepereted_term(removal)")
    print( "+")
    print( regex_to_big_query(build_sepereted_term(removal)))

    print( "# Refactor :build_refactor_goals_regex()")
    print( "+")
    print( regex_to_big_query(build_refactor_goals_regex()))


def non_code_refactor_to_bq():
    print( "# Refactor :build_non_code_perfective_regex()")
    print( regex_to_big_query(build_non_code_perfective_regex()))

def non_positive_linguistic_refactor_to_bq():
    print( "# Refactor :build_non_positive_linguistic(build_refactor_regex())")
    print( "-")
    print( regex_to_big_query(build_non_positive_linguistic(build_refactor_regex(use_conventional_commits=False))))

def non_positive_linguistic_refactor_goals_to_bq():
    print( "# Refactor :build_non_positive_linguistic(build_refactor_goals_regex())")
    print( regex_to_big_query(build_non_positive_linguistic(build_refactor_goals_regex())))

def non_positive_linguistic_removal_to_bq():
    print("# Refactor :build_non_positive_linguistic(build_sepereted_term(removal))")
    print(regex_to_big_query(build_non_positive_linguistic(build_sepereted_term(removal))))


def documentation_entities_context_refactor_to_bq():
    print("# Refactor :build_documentation_entities_context(build_refactor_regex())")
    print(regex_to_big_query(
        build_documentation_entities_context(build_refactor_regex(use_conventional_commits=False))))



def refactor_to_bq():

    print( "# Refactor")

    print('{schema}.bq_positive_refactor(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_code_refactor(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_positive_linguistic_refactor(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_positive_linguistic_refactor_goals(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_positive_linguistic_refactor_removal(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_documentation_entities_context_refactor(message)'.format(schema=SCHEMA_NAME))

    print( "# Refactor - end ")


def built_is_refactor(commit_text):
    removal_re = build_sepereted_term(removal)

    return (match(commit_text, build_refactor_regex())
            + match(commit_text, removal_re)
            + match(commit_text, build_refactor_goals_regex())
            - match(commit_text, build_non_code_perfective_regex())
            - match(commit_text
                    , build_documentation_entities_context(build_refactor_regex(use_conventional_commits=False)))
            - match(commit_text
                    , build_non_positive_linguistic(build_refactor_regex(use_conventional_commits=False)))
            - match(commit_text, build_non_positive_linguistic(build_sepereted_term(removal)))
            - match(commit_text, build_non_positive_linguistic(build_refactor_goals_regex()))
            ) > 0

def build_perfective_regex():
    non_code = build_sepereted_term (prefective_entities)

    perfective = "(%s)" %  non_code

    return perfective


def just_perfective_to_bq():

    print("# Just Perfective")
    print( "# Perfective :build_perfective_regex()")
    #print( ",")
    print( regex_to_big_query(build_perfective_regex()))

def perfective_to_bq():

    print( "# Perfective")

    print('{schema}.bq_just_perfective(message)'.format(schema=SCHEMA_NAME))
    print(' + {schema}.bq_refactor(message)'.format(schema=SCHEMA_NAME))

    print( "# Perfective - end ")



def print_refactor_functions(commit: str = 'XXX'):

    generate_bq_function('{schema}.bq_core_refactor'.format(schema=SCHEMA_NAME)
                         , core_refactor_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_positive_refactor'.format(schema=SCHEMA_NAME)
                         , positive_refactor_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_non_code_refactor'.format(schema=SCHEMA_NAME)
                         , non_code_refactor_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_non_positive_linguistic_refactor'.format(schema=SCHEMA_NAME)
                         , non_positive_linguistic_refactor_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_non_positive_linguistic_refactor_goals'.format(schema=SCHEMA_NAME)
                         , non_positive_linguistic_refactor_goals_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_non_positive_linguistic_refactor_removal'.format(schema=SCHEMA_NAME)
                         , non_positive_linguistic_removal_to_bq
                         , commit=commit)
    print()


    generate_bq_function('{schema}.bq_documentation_entities_context_refactor'.format(schema=SCHEMA_NAME)
                         , documentation_entities_context_refactor_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_refactor'.format(schema=SCHEMA_NAME)
                         , refactor_to_bq
                         , commit=commit)
    print()

    print()

    generate_bq_function('{schema}.bq_just_perfective'.format(schema=SCHEMA_NAME)
                         , just_perfective_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_perfective'.format(schema=SCHEMA_NAME)
                         , perfective_to_bq
                         , commit=commit)
    print()

if __name__ == '__main__':
    print_refactor_functions(commit='4b76d8e76af938824f91f4b99247731c21e37ff9')