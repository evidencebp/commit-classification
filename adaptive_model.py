
from language_utils import file_scheme, term_seperator, build_sepereted_term, negation_terms, modals\
    , regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, documentation_entities, prefective_entities\
    , software_terms, build_non_positive_linguistic, software_goals_modification, software_goals, unnedded_terms

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


adaptive_entities = ['ability', 'configuration', 'conversion', 'debug', 'new', 'possibility', 'support'
    , 'test(s)?', 'tweak(s)?', 'mode', 'option']


adaptive_header_action = "|".join([
    'upgrad(?:e|es|ed|ing)',
    'configur(?:e|es|ed|ing)',
    '(?:keep|change)\s+(?:the\s+)?default',
    'new',
    # 'merg(?:e|es|ed|ing)',
    # '(?:make(?:s)?|made|making)',
    # 'merg(?:e|es|ed|ing)',
    'clear(?:s|ed|ing)?',
    # 'convert(?:s|ed|ing)?',
    # 'check(?:s|ed|ing)?',
    'add(?:s|ed|ing)?',
    # 'build',
    # 'buil(?:d|t|ds|ing)',
    '(?:im)?port(?:s|ed|ing)?',
    '(?:un)?hid(?:e|es|den)',
    'updat(?:e|es|ed|ing)',
    'disabl(?:e|es|ed|ing)',
    'enabl(?:e|es|ed|ing)',
    'quirk(?:s|ed|ing)?',
    'allow(?:s|ed|ing)?',
    'provid(e|es|ed|ing)',
    # 'remov(e|es|ed|ing)'

    ###
    # , 'build'
    # , 'mark(?:s|ed|ing)?'
    # , 'us(?:e|es|ed|ing)'
    # , '(?:make|made|making)'
    # , 'chang(?:e|es|ed|ing)'
    # , 'creat(?:e|es|ed|ing)'
    # , 'enabl(?:e|es|ed|ing)'
    # , 'handl(?:e|es|ed|ing)'
    'remov(?:e|es|ed|ing)'

])

adaptive_actions = [  # 'revert(?:s|ed|ing)?',
    #'merg(?:e|es|ed|ing)[\s\S]{1,5}(pull request|pr|branch)',
    'add(?:s|ed|ing)?[\s\S]{1,50}(?:version|v\d|ver\d)',
    '(^|\s)implement(?:ed|s|ing)?\s',
    '(?:make(?:s)?|made|making)[\s\S]{1,50}consitent',
    'updat(?:e|es|ed|ing)[\s\S]{1,25}to[\s\S]{1,25}\d+.\d',
    'updat(?:e|es|ed|ing)\s+(to\s+)?\d+\.\d',
    '(?:add(s|ed|ing)?|delet(?:e|es|ed|ing)|updat(?:e|es|ed|ing))\s+' + file_scheme,
    # '(add(s|ed|ing)?|delet(e|es|ed|ing)|updat(e|es|ed|ing))\s+([A-Z0-9_]*)', # TODO - run without lower
    '(^|^[\s\S]{0,25}%s)(%s)%s' % (term_seperator, adaptive_header_action, term_seperator),
    # '^(?:version|v\d+\.\d|ver\d+\.\d)',
    '^\[(?:IMP|imp)\]',  # TODO - take care of upper/lower case
    'support(?:s|ed|ing)?\sfor\s',
    'show(?:es|ed|ing)?[\s\S]instead']


def build_adaptive_action_regex():

    return "(%s)" % ("|".join(
    adaptive_actions))




def build_adaptive_regex():

    adaptive_context_re = build_sepereted_term(adaptive_context, just_before=True)


    return "((%s)\s[\s\S]{0,50}(%s)%s)" % (adaptive_context_re
                            ,  "|".join(adaptive_entities + software_terms)
                            , term_seperator)



def build_non_adaptive_context():

    non_adaptive_header_action = "|".join([
                                'transla(?:tion|et|eted|ets|ting)'
                                ,  'readme(?:.md)?'
                              ])

    non_adaptive_header ='^[\s\S]{0,50}(%s)' % non_adaptive_header_action

    entities = documentation_entities + ['bug',
                'helper',
                'miss(?:ing|ed)',
                'to(?: |-)?do(?:s)?',
                'warning(?:s)?'
                ]

    adaptive_actions = ['remov(?:e|es|ed|ing)']
    non_adaptive_entities = documentation_entities + software_terms + unnedded_terms + [file_scheme]


    return '(%s)' % "|".join(['(?:%s)\s[\s\S]{0,50}(?:%s)' % (build_sepereted_term(adaptive_context, just_before=True)
                                                            , "|".join(entities))
                     , non_adaptive_header
                     , '(?:%s)\s[\s\S]{0,50}(?:%s)' % (build_sepereted_term(adaptive_actions, just_before=True)
                                                            , "|".join(non_adaptive_entities))
                     ])


def build_non_adaptive_linguistic():

    return build_non_positive_linguistic(build_adaptive_regex())

def is_adaptive(text):

    return (match(text, build_adaptive_regex())
            + match(text, build_adaptive_action_regex())
            - match(text, build_non_adaptive_context())
            - match(text, build_non_adaptive_linguistic()))

def adaptive_to_bq():


    print("# Adaptive")
    print( "# Adaptive :build_adaptive_regex()")
    #print( ",")
    print( regex_to_big_query(build_adaptive_regex()))
    print( "#Adaptive :build_adaptive_action_regex()")
    print( "+")
    print( regex_to_big_query(build_adaptive_action_regex()))
    print( "# Adaptive :build_non_adaptive_context()")
    print( "-")
    print( regex_to_big_query(build_non_adaptive_context()))
    print( "# Adaptive :build_non_adaptive_linguistic()")
    print( "-")
    print( regex_to_big_query(build_non_adaptive_linguistic()))
    print("# Adaptive - end")


def print_adaptive_functions():
    print()
    generate_bq_function('{schema}.bq_adaptive'.format(schema=SCHEMA_NAME), adaptive_to_bq)
    print()


if __name__ == '__main__':
    print_adaptive_functions()