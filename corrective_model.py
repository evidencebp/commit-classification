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
from conventional_commits import build_cc_corrective_regex
from labeling_util import get_false_positives, get_false_negatives

from language_utils import file_scheme, term_seperator, build_sepereted_term, negation_terms, modals\
    , regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, documentation_entities, prefective_entities\
    , static_analyzers, NEAR_ENOUGH, software_entities, code_review_fixes, normalize
from model_evaluation import classifiy_commits_df, evaluate_performance

# TODO - use split to find related tokens
#  https://stackoverflow.com/questions/27060396/bigquery-split-returns-only-one-value/27158310

# NPE, prevent, incompatible, roll back, nullptr, NullPointerException
# Table 1 in "A Comparative Study of Industrial Static
# Analysis Tools"
# https://www.sans.org/top25-software-errors/
"""
To consider
I forgot, forever, infinite loop

Should conventional commits overide all - fix(postcss): filter conflicting order warnings

Fix changes merge for 3450
Fix spelling
Fix concurrency issues with CQL keyspace creation
Make sure DeletedColumn.isMFD always return true
Always use RANGE_SLICE verb for 3.x messages
NullPointerException during compaction on table with static columns
"""
core_bug_terms = [
             'bug(s|z)?',
             'bug(?:-|\s)?fix(es)?',
             'defect(?:s)?',
             'error(?:s)?',
             'failur(?:ing|e|es|ed)',
             'fault(s)?',
             'fix(ed|es|ing)?',
             'fixing(?:s)?',
             'incorrect(ly)?',
             'mistake(s|n|d|nly)?',
             'problem(?:s)?',
             ]
# Positive
bug_terms = ['actual.*expected',
             '((assignment|assign|=) in if|== instead of =)', # condition/conditional is usually a static analyzer warning
             'expected.*actual'
             '(choose|take|set|use)\\s*(the|a)?\\s*correct', # correct as adjective
             "(not|isn't|doesn't)\\s+work(s|ing)?", # TODO - check with negation
             "doesn't recognize", # TODO Extend
             'double(?:-| )allocat(?:e|ion|ions)',
             'double(?:-| )free(?:s)?',
             "caused a regression", # TODO Extend
             'bad initialization(?:s)?',
             'buffer overflow(?:s)?',
             'fixme(?:s)?',
             'fixes(?:-| )?commit(?::| )?',
             '(break|breaks|broke|broked|breaking|broken)[\s\S]{0,20}(code|system|function|method)',
             '(this|that|it)\s(break|breaks|broke|broked|breaking|broken)',
             'break strict(?:-|\s)aliasing rule(s)?',
             'crash(?:ing|s|ed)?',
             'correct(?:ing|s|ed)?\\s*(a|the|some|few|this)', # make sure that correct serves as a verb
             'correct(ed|ion|ly|s)?',
             '(dangling|hanging) pointer(?:s)?',
             'deadlock(?:s)?',
             '(divid(e|es|ed|ing)|division) by (zero|0)',
             'double(?:-| )free',
             'fail(?:ing|s|ed)?',
             'faulty initialization(?:s)?',
             'fix(?:-| )?in(?:s)?',
             'fix(?:-| )?up(?:s)?',
             'flaw(?:s|ed)?',
             '(float|integer) (under|over)(?:-| )?flow',
             'hot(?:-| )?fix(?:ed|es|ing)?',
             #'hang',
             'heap overflow(?:s)?',
             '(?:im|im-)?proper'
             'memory(?:-| )?leak(?:s)?',
             'missing\s(default value|initialization|switch case)(?:s)?',
             'is\smissing',
             'add(?:ing|s|ed)?\smiss(?:ing|es|ed)?',
             #'must not',
             'npe(?:s)?'
             'null pointer(?:s)?',
             'nullpointerexception',
             #'[a-z]+exception', # finds new cases but filtering is needed
             'off(?:-| )by(?:-| )(one|1)',
             'out of bound(?:s)?',
             'over(?:-| )?run(?:s)?',
             'patch(?:ed|ing)',
             #'prevent(?:ing|s|ed)?', # should be tuned
             'race condition(?:s)?',
             'data race(?:s)?',
             'repair(?:ing|s|ed)?',
             'resource leak(?:s)?',
             # TODO - check generalization to leaks works in the other direction to expected (reduces FP, increases FN)
             'leak(?:s)?',
             'revert(?:ing|s|ed)?',
             'segmentation (fault|violation)(?:s)?',
             'resolv(?:ing|e|es|ed)',
             #'solv(?:ing|e|es|ed)',
             'workaround(?:s)?',
             'wrong(nly)?',
             '(type(s)? mis(?:-| )?match|(not|non|none) matching type(s)?)',
             'trouble(?:s)?',
             '(un(?:-| )?|not )initialized variable(s)?',
             'unintended',
             'not intended',
             'unintentionally',
             'not intentionally',
             # 'unexpected.*occurred', # very rare, 90% are bugs anyway
             'vulnerabilit(?:y|ies)'
             ] + core_bug_terms

# Valid_fix_objects
valid_fix_object = prefective_entities + ['#',
                    '(camel|snake|kebab|flat|lower|upper)\\s*case',
                    "code review('s|s)?",
                    'comment(?:s)?',
                    'cosmetic(?:s)?',
                    'cr(s)?(?:-)?',
                    'documentation(?:s)?',
                    #'exception(?: |-)?handling',
                    #'format(s|ing)? fix(ed|es|ing)?',
                    'format(?:ing)?',
                    'help',
                    'remark(s)?',
                    'spac(e|es|ing)',
                    'spelling',
                    'style|styling',
                    'typo(s)?',
                    'typing(?: |-)?(error|mistake)(s)?',
                    'warning(s)?',
                    'white(?: |-)?spac(?:e|es|ed|ing)',
                                          ]

valid_terms = [
    'break\sout',
    'error(?: |-)?check(ing)?',
    'error(?: |-)?handling',
    'error message(s)?',
    'error report(s|ing)?',
    'fixed(?: |-)?point',
    'fix(?:ed) ticket(?:s)?',
    #'format(ing)?',
    '(?:fix(?:ed|es)?|bug)(?: )?(?: |-|=|:)(?: )?[a-z]{0,3}(?:-)?\d+' + term_seperator,
    '(?:fix(?:ed|es)?|bug)(?:-|=|:)\d+',
    '(if|would)[\s\S]{0,40}go wrong',
    'line(?:s)? break(?:s)?',
    'typo(s)?\sfix(es)?',
    'fix(ed|es|ing)?' + build_sepereted_term(software_entities) + 'name(s)?',
    build_sepereted_term(static_analyzers) + 'fix(es|ed)?',
    'fix(es|ed)?' + build_sepereted_term(static_analyzers) ,
    '^### Bug Fix', # tends to be a title, later stating if the commit is a bug fix
    'edit the jira link to the correct issue', # Another occurring title
    'page(?:s)? break(?:s)?',
    'fix changes merge',
    '(understand|understood)\scorrectly',


] + code_review_fixes



fixing_verbs = ['correct(?:ing|s|ed)'
                    , 'fix(ed|s|es|ing)?'
                    , 'repair(?:ing|s|ed)?'
                    ,  'revert(?:ing|s|ed)?'
                    , 'resolv(?:ing|e|es|ed)'
                    , 'revok(?:ing|e|es|ed)'
                    , 'und(?:oing|id)'
                ]
MERGE_PREFIX = '(merge (branch|pull request).{0,25}|merge (branch|pull request).{0,25}(from|into).{0,25})'
END_OF_LINE = r'(\r\n|\r|\n|$)'
corrective_header_entities = fixing_verbs + [
    'miss(?:ing|es|ed)?', 'should', 'must', '(have|has) to', 'avoid', 'prevent', 'break(s|ed|ing)?', 'broken'
    , 'remov(?:ing|e|es|ed) change(?:s)?', 'unable', 'proper(?:ly)?'
    , MERGE_PREFIX + "(%s)" % "|".join(core_bug_terms) + '.{0,250}' + END_OF_LINE
    #, "(does not|doesn't) need" , "cannot", "can not"
 ] #+ [ "do not" ,"don't", "dont"]

def build_valid_find_regex():
    fix_re = "(" + "|".join(fixing_verbs + [MERGE_PREFIX]) + ")"
    prefix = term_seperator + fix_re + '[\s\S]{1,40}' + "(" + "|".join(valid_fix_object) + ")" + term_seperator

    suffix = term_seperator + "(" + "|".join \
        (valid_fix_object) + ")" + term_seperator + '[\s\S]{0,40}'  + fix_re + term_seperator

    # TODO - check seperation
    #sepertion = '(?:%s|%s[\s\S]{0,40}%s)' % (term_seperator, term_seperator, term_seperator)
    #suffix = "(" + "|".join \
    #    (valid_fix_object) + ")" + sepertion + fix_re + term_seperator

    #other_valid_re = "(%s)" % "|".join(valid_terms)
    other_valid_re = build_sepereted_term(valid_terms)
    return "((%s)|(%s)|(%s))" % (prefix, suffix, other_valid_re)


def build_bug_fix_regex(use_conventional_commits=True):
    header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)%s' % (term_seperator
                                                       , "|".join(corrective_header_entities)
                                                       , term_seperator)
   # strict_header = "^(?:%s)%s"  % ( "|".join([ "do not" ,"don't"])
   #                                                    , term_seperator)

    bug_fix_re = build_sepereted_term(bug_terms)


    if use_conventional_commits:
        agg_re = "((%s)|(%s)|(%s))" % (bug_fix_re, header_regex, build_cc_corrective_regex())
    else:
        agg_re = "((%s)|(%s))" % (bug_fix_re, header_regex)

    return agg_re

def build_negeted_bug_fix_regex():
    bug_fix_re = build_bug_fix_regex(use_conventional_commits=False)
    negation_re = build_sepereted_term(negation_terms)


    return "%s[\s\S]{0,20}%s" % (negation_re, bug_fix_re)


def build_core_bug_regex():

    return '(%s)' % build_sepereted_term(core_bug_terms)

def is_core_bug(commit_text):
    text = commit_text.lower()

    cnt = len(re.findall(build_core_bug_regex(), text))

    return cnt > 0

def is_fix(commit_text):

    text = commit_text.lower()
    #text = normalize(text)

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



def print_corrective_functions(commit: str = 'XXX'):
    print()
    generate_bq_function('{schema}.bq_corrective'.format(schema=SCHEMA_NAME)
                         , corrective_to_bq
                         , commit=commit)
    print()


def core_bug_to_bq():
    # TODO - the \n in the string seperator is printed as a new line and should be fixed
    print("# Core Bug Term")
    print( regex_to_big_query(build_core_bug_regex()))
    print("#Core Bug Term - end")



def print_core_bug_function(commit: str = 'XXX'):
    print()
    generate_bq_function('{schema}.bq_core_bug'.format(schema=SCHEMA_NAME)
                         , core_bug_to_bq
                         , commit=commit)
    print()

def evaluate_fix_classifier():


    text_name = 'message'
    classification_function = is_fix
    classification_column = 'corrective_pred'

    concept_column='Is_Corrective'

    df = pd.read_csv(join(DATA_PATH, 'corrective_texts_tests.csv'))
    
    #df = df[df.certain != 'FALSE']
    df = df[~df.Is_Corrective.isna()]

    #concept_column='is_corrective'
    #df = pd.read_csv("/Users/idan/playground/commit-classification/data/change_samples.csv")


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
    df = df[(df['disable'] != 1)]
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
    #for _, i in fn.iterrows():
    #    print(i.commit, i.message)


if __name__ == '__main__':

    print_corrective_functions(commit='4b76d8e76af938824f91f4b99247731c21e37ff9')
    print_core_bug_function(commit='4b76d8e76af938824f91f4b99247731c21e37ff9')
    evaluate_fix_classifier()
    #this fixed the bug 123

    text = """added whitespace fix""".lower()
    print("is fix", is_fix(text))
    print("fix in text", re.findall(build_bug_fix_regex(), text))
    print("v1", re.findall('white(?: |-)?spac(?:e|es|ed|ing)', text))

    fix_re = "(" + "|".join(fixing_verbs + [MERGE_PREFIX]) + ")"

    suffix = term_seperator + "(" + "|".join \
        (valid_fix_object) + ")" + term_seperator + '[\s\S]{0,40}' + term_seperator + fix_re #+ term_seperator

    print("v2", re.findall(suffix, text))
    print("v3", re.findall(term_seperator + "(" + "|".join(valid_fix_object) + ")" + term_seperator + '[\s\S]{0,40}' + term_seperator + fix_re, text))
    print("v4", re.findall(  "(" + "|".join(valid_fix_object) + ")" + '[\s\S]{0,40}' + term_seperator + fix_re, text))
    valid_num = len(re.findall(build_bug_fix_regex(), text))
    #print(re.findall(r'(merge (branch|pull request).{0,250}(\r\n|\r|\n|$)|merge (branch|pull request).{0,250}(from|into).{0,250}(\r\n|\r|\n|$))'fix', text))

    print(valid_num)
    print(build_negeted_bug_fix_regex())
