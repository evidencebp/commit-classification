import re
from os.path import join
import pandas as pd

from configuration import DATA_PATH

from labeling_util import get_false_positives, get_false_negatives

from language_utils import file_scheme, term_seperator, build_sepereted_term, negation_terms, modals\
    , regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, documentation_entities, prefective_entities\
    , software_terms, build_non_positive_linguistic, software_goals_modification, software_goals, unnedded_terms\
    , code_review_fixes, no_message, NEAR_ENOUGH

from model_evaluation import classifiy_commits_df, evaluate_performance

core_adaptive_terms = [
    'add(?:s|ed|ing)?',
    'creat(?:e|es|ing)',
    'disabl(?:e|es|ed|ing)',
    'implement(?:ed|s|ing)?',
    'import(?:s|ed|ing)?',
    'introduc(?:e|es|ed|ing)',
    'port(?:s|ed|ing)?',
    'provid(?:e|es|ed|ing)',
    'updat(?:e|es|ed|ing)',
    'upgrad(?:e|es|ed|ing)'

]

adaptive_context = [
 '(?:un)?hid(?:e|es|den)',
 'allow(?:s|ed|ing)?',
 'buil(?:t|ds|ing)',
 'calibirat(?:e|es|ed|ing)',
 'configure',
 'deferr(?:ed|s|ing)?',
 'enhanc(?:e|es|ed|ing)',
 'extend(?:s|ed|ing)?',
 'form(?:ed|s|ing)?',
 'report(?:s|ed|ing)?',
 'support(s|ed|ing)?',

# , 'mov(e|es|ed|ing)'
# , 'print(s|ed|ing)?'

] + core_adaptive_terms



adaptive_entities = ['ability', 'configuration', 'conversion', 'debug', 'new', 'possibility', 'support'
    , 'test(s)?', 'tweak(s)?', 'mode', 'option']


adaptive_header_action = "|".join([
    'upgrad(?:e|es|ed|ing)',
    'configur(?:e|es|ed|ing)',
    'chang(?:e|es|ed|ing)',
    '(?:keep|change)\s+(?:the\s+)?default',
    'new',
    # '(?:make(?:s)?|made|making)',
    'merg(?:e|es|ed|ing)',
    'clear(?:s|ed|ing)?',
    #'comment(?:s|ed|ing)?\sout'
    'creat(?:e|es|ed|ing)',
    'cast(?:s|et|ing)?' + NEAR_ENOUGH + '\sas',
    # 'convert(?:s|ed|ing)?',
    # 'check(?:s|ed|ing)?',
    'add(?:s|ed|ing)?',
    # 'buil(?:d|t|ds|ing)',
    'Initial revision',
    '(?:im)?port(?:s|ed|ing)?',
    '(?:un)?hid(?:e|es|den)',
    'updat(?:e|es|ed|ing)',
    'upload(?:s|ed|ing)?',
    'disabl(?:e|es|ed|ing)',
    'delet(?:e|es|ed|ing)',
    'enabl(?:e|es|ed|ing)',
    'quirk(?:s|ed|ing)?',
    'skip(?:s|ed|ing)?',
    'switch(?:s|ed|ing)?',
    'allow(?:s|ed|ing)?',
    'provid(e|es|ed|ing)',

    ###
    # , 'build'
    # , 'mark(?:s|ed|ing)?'
    # , 'us(?:e|es|ed|ing)'
    # , '(?:make|made|making)'
    # , 'creat(?:e|es|ed|ing)'
    # , 'handl(?:e|es|ed|ing)'
    'remov(?:e|es|ed|ing)',
    'refresh(?:s|ed|ing)?',
    #'re(-)?enabl(?:e|es|ed|ing)',

] +no_message
)

adaptive_actions = [  # 'revert(?:s|ed|ing)?',
    #'merg(?:e|es|ed|ing)[\s\S]{1,5}(pull request|pr|branch)',
    'add(?:s|ed|ing)?[\s\S]{1,50}(?:version|v\d|ver\d)',
    #'(cr(s)?(-)?|code\sreview)\sfix(?:s|ed|ing)?',
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
    'show(?:es|ed|ing)?[\s\S]instead',
    'scal(?:e|es|ed|ing)?\s(up|down)'

                   ] + code_review_fixes


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



def build_core_adaptive_regex():

    return '(%s)' % build_sepereted_term(core_adaptive_terms)


def core_adaptive_to_bq():
    print("# Core Adaptive Term")
    print( regex_to_big_query(build_core_adaptive_regex()))
    print("#Core Adaptive Term - end")


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


def print_adaptive_functions(commit: str = 'XXX'):
    print()
    generate_bq_function('{schema}.bq_adaptive'.format(schema=SCHEMA_NAME)
                         , adaptive_to_bq
                         , commit=commit)
    print()

    core_adaptive_to_bq
    print()

    generate_bq_function('{schema}.bq_core_adaptive'.format(schema=SCHEMA_NAME)
                         , core_adaptive_to_bq
                         , commit=commit)
    print()


def evaluate_adaptive_classifier():
    text_name = 'message'
    classification_function = is_adaptive
    classification_column = 'corrective_pred'

    concept_column='Is_Adaptive'

    df = pd.read_csv(join(DATA_PATH, 'commit_classification_batch2.csv'))
    df = df[df.certain != 'FALSE']
    df = df[~df.Is_Corrective.isna()]

    """
    concept_column = 'is_adaptive'
    df = pd.read_csv(join(DATA_PATH, "commit_classification_batch2.csv"))
    df[concept_column] = df.expected.map(lambda x: not x)
    """
    df = classifiy_commits_df(df
                              , classification_function=classification_function
                              , classification_column=classification_column
                              , text_name=text_name
                              )
    cm = evaluate_performance(df
                              , classification_column
                              , concept_column
                              , text_name=text_name)
    print("corrective_labels CM")
    print(cm)
    """
    fp = get_false_positives(df
                             , classifier_column=classification_column
                             , concept_column=concept_column)
    print("False Positives")
    pd.options.display.max_columns = 50
    pd.options.display.max_rows = 2000
    print(fp)

    """
    fn = get_false_negatives(df
                        , classifier_column=classification_column
                        , concept_column=concept_column)
    print("False Negatives")
    pd.options.display.max_columns = 50
    pd.options.display.max_rows = 2000
    print(fn)



if __name__ == '__main__':
    print_adaptive_functions(commit='fd01abaffc30965f113a30bc97e9a83d9beec50d')
    evaluate_adaptive_classifier()

    text = """Update values-prod-tags.yaml""".lower()
    print(is_adaptive(text))
    valid_num = len(re.findall(build_adaptive_action_regex(), text))
    valid_num = len(re.findall('updat(?:e|es|ed|ing)', text))
    valid_num = len(re.findall(build_non_adaptive_context(), text))



    print(valid_num)
    print(build_non_adaptive_context())
