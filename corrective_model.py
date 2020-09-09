"""
This file contain a python implementation of the corrective commit linguistic model
and the English linguistic model.
While the model used in the research was implementer in a BigQuery implementation,
the python implementation is valuable.
First, it enable to structure the model and export it for BigQuery.
Other than that, it enable running the model on test and other examples.
Running it on the train set iteratively enabled rapid evaluation of the model.

BigQuery uses the re2 engine for regular expressions, since it is fast.
This prevented us from using lookaheads and lookbehinds, which are not supported.



"""

import re
from os.path import join
import pandas as pd

from configuration import DATA_PATH

from labeling_util import get_false_positives, get_false_negatives

from language_utils import file_scheme, term_seperator, build_sepereted_term, negation_terms, modals\
    , regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, documentation_entities, prefective_entities\
    , static_analyzers, NEAR_ENOUGH, software_entities
from model_evaluation import classifiy_commits_df, evaluate_performance

# TODO - use split to find related tokens
#  https://stackoverflow.com/questions/27060396/bigquery-split-returns-only-one-value/27158310

# Positive
bug_terms = ['(choose|take|set|use)\\s*(the|a)?\\s*correct', # correct as adjective
             "(not|isn't|doesn't)\\s+work(s|ing)?", # TODO - check with negation
             "doesn't recognize", # TODO Extend
             "caused a regression", # TODO Extend
             'bad initialization(?:s)?',
             'buffer overflow(?:s)?',
             'bug(s|z)?',
             'bug(?:-| )?fix(es)?',
             '(break|broke|breaking|broken)[\s\S]{0,20}(code|system|function|method)',
             'crash(?:ing|s|ed)?',
             'correct(?:ing|s|ed)?\\s*(a|the|some|few|this)', # make sure that correct serves as a verb
             'correct(ed|ion|ly|s)?',
             'dangling pointer(?:s)?',
             'deadlock(?:s)?',
             'defect(?:s)?',
             'double(?:-| )free',
             'error(?:s)?',
             'fail(?:ing|s|ed)?',
             'failur(?:ing|e|es|ed)',
             'fault(s)?',
             'faulty initialization(?:s)?',
             'fix(ed|es|ing)?',
             'fix(?:-| )?in(?:s)?',
             'fixing(?:s)?',
             'fix(?:-| )?up(?:s)?',
             'flaw(?:s|ed)?',
             #'hang',
             'heap overflow(?:s)?',
             'incorrect(ly)?',
             '(?:im|im-)?proper'
             'memory(?:-| )?leak(?:s)?',
             'missing\s(default value|initialization|switch case)(?:s)?',
             'add(?:ing|s|ed)?\smiss(?:ing|es|ed)?',
             'mistake(s|n|nly)?',
             #'must not',
             'null pointer(?:s)?',
             'over(?:-| )?run(?:s)?',
             'patch(?:ed|ing)',
             'problem(?:s)?',
             'race condition(?:s)?',
             'data race(?:s)?',
             'repair(?:ing|s|ed)?',
             'resource leak(?:s)?',
             # TODO - check generalization to leaks works in the other direction to expected (reduces FP, increases FN)
             'leak(?:s)?',
             'revert(?:ing|s|ed)?',
             'segmentation fault(?:s)?',
             'resolv(?:ing|e|es|ed)',
             #'solv(?:ing|e|es|ed)',
             'workaround(?:s)?',
             'wrong(nly)?',
             'trouble(?:s)?',
             'vulnerabilit(?:y|ies)']

# Valid_fix_objects
valid_fix_object = prefective_entities + ['#',
                    '(camel|snake|kebab|flat|lower|upper)\\s*case',
                    "code review('s|s)?",
                    'comment(?:s)?',
                    'cosmetic(?:s)?',
                    'cr(s)?(-)?',
                    'documentation(?:s)?',
                    'format(s|ing)?',
                    'help',
                    'remark(s)?',
                    'space(s)?',
                    'style|styling',
                    'typo(s)?',
                    'typing(?: |-)?(error|mistake)(s)?',
                    'warning(s)?',
                    'white(?: |-)?space(s)?']

valid_terms = [
    'error(?: |-)?check(ing)?',
    'error(?: |-)?handling',
    'error message(s)?',
    'error report(s|ing)?',
    'exception(?: |-)?handling',
    'fixed(?: |-)?point',
    'fix(?:ed) ticket(?:s)?',
    '(?:fix(?:ed)?|bug)(?: )?(?: |-|:)(?: )?\d+',
    '(if|would)[\s\S]{0,40}go wrong',
    '(cr|pr)(s)?(-)?(d+)?\sfix(es)?',
    'typo(s)?\sfix(es)?',
    'fix(ed|es|ing)?' + build_sepereted_term(software_entities) + 'name(s)?',
    build_sepereted_term(static_analyzers) + 'fix(es|ed)?',
    '^### Bug Fix', # tends to be a title, later stating if the commit is a bug fix
    'edit the jira link to the correct issue', # Another occurring title

]



fixing_verbs = ['correct(?:ing|s|ed)'
                    , 'fix(ed|s|es|ing)?'
                    , 'repair(?:ing|s|ed)?'
                    ,  'revert(?:ing|s|ed)?'
                    , 'resolv(?:ing|e|es|ed)'
                ]

corrective_header_entities = fixing_verbs + [
    'miss(?:ing|es|ed)?', 'should', 'must', '(have|has) to', 'avoid', 'prevent', 'break(s|ed|ing)?', 'broken'
    #, "(does not|doesn't) need" , "cannot", "can not"
 ] #+ [ "do not" ,"don't"]

def build_valid_find_regex():
    fix_re = "(" + "|".join(fixing_verbs) + ")"
    prefix = term_seperator + fix_re + '[\s\S]{1,40}' + "(" + "|".join(valid_fix_object) + ")" + term_seperator

    suffix = "(" + "|".join \
        (valid_fix_object) + ")" + term_seperator + '[\s\S]{0,40}' + term_seperator + fix_re + term_seperator

    # TODO - check seperation
    #sepertion = '(?:%s|%s[\s\S]{0,40}%s)' % (term_seperator, term_seperator, term_seperator)
    #suffix = "(" + "|".join \
    #    (valid_fix_object) + ")" + sepertion + fix_re + term_seperator

    other_valid_re = "(%s)" % "|".join(valid_terms)

    return "((%s)|(%s)|(%s))" % (prefix, suffix, other_valid_re)


def build_bug_fix_regex():
    header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)%s' % (term_seperator
                                                       , "|".join(corrective_header_entities)
                                                       , term_seperator)
   # strict_header = "^(?:%s)%s"  % ( "|".join([ "do not" ,"don't"])
   #                                                    , term_seperator)

    bug_fix_re = build_sepereted_term(bug_terms)

    return "((%s)|(%s))" % (bug_fix_re, header_regex)
    #return "((%s)|(%s)|(%s))" % (bug_fix_re, header_regex, strict_header)

def build_negeted_bug_fix_regex():
    bug_fix_re = build_bug_fix_regex()
    negation_re = build_sepereted_term(negation_terms)


    return "%s[\s\S]{0,20}%s" % (negation_re, bug_fix_re)



def is_fix(commit_text):

    text = commit_text.lower()

    fix_num = len(re.findall(build_bug_fix_regex(), text))
    valid_num = len(re.findall(build_valid_find_regex(), text))
    negated_num = len(re.findall(build_negeted_bug_fix_regex(), text))
    # TODO  consider modals
    #negated_num = len(re.findall(build_non_positive_linguistic(build_bug_fix_regex()), text))
    return (fix_num - valid_num - negated_num) > 0
    #return (fix_num ) > 0 # max recall with current predictor

def corrective_to_bq():
    # TODO - the \n in the string seperator is printed as a new line and should be fixed
    print("# Corrective")
    print( "# Corrective : build_bug_fix_regex()")
    #print( ",")
    print( regex_to_big_query(build_bug_fix_regex()))
    print(" - ")
    print( "# Corrective : build_valid_find_regex()")
    print( regex_to_big_query(build_valid_find_regex()))
    print(" - ")
    print( "# Corrective : build_negeted_bug_fix_regex()")
    print( regex_to_big_query(build_negeted_bug_fix_regex()))
    print("#Corrective - end")



def print_corrective_functions():
    print()
    generate_bq_function('{schema}.bq_corrective'.format(schema=SCHEMA_NAME), corrective_to_bq)
    print()

def evaluate_fix_classifier():


    text_name = 'message'
    classification_function = is_fix
    classification_column = 'corrective_pred'
    concept_column='expected'

    df = pd.read_csv(join(DATA_PATH, 'corrective_labels.csv'))
    df = df[df.uncertain != 'TRUE']

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

    #print_corrective_functions()
    evaluate_fix_classifier()
    text = """Merge branch 'master' into DEV-21847-fix-metrics-alerts-fail-to-send-pagerduty-payload-due-to-blank-description""".lower()
    print(is_fix(text))
    valid_num = len(re.findall(build_bug_fix_regex(), text))


    valid_num = len(re.findall('(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|\-|/)' + "fix" , text))
    valid_num = len(re.findall(term_seperator + "fix" + term_seperator , text))
    valid_num = len(re.findall("(=|\-)fix(=|\-)" , text))
    print(valid_num)
    print(build_bug_fix_regex())
