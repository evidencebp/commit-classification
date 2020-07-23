import re
from typing import List

regex_list : List[str]

SCHEMA_NAME = 'general'
file_scheme = '([a-z  -Z0-9_\*\.])+\.[a-zA-Z]{1,4}'

term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|\'|\"|/|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|\|)"

def build_sepereted_term(term_list : List, just_before =False):
    if just_before:
        sep = "%s(%s)" % (term_seperator, "|".join(term_list))
    else:
        sep = "%s(%s)%s" % (term_seperator, "|".join(term_list), term_seperator)
    return sep


# Negation
negation_terms = ["aren't", "didn't" ,"don't", "doesn't", "isn't", 'lack', "n't", 'never', 'no', 'nobody', 'none', 'not'
    , 'nothing', "weren't", 'without', "won't"]

modals = ['can', 'could', 'ha(?:ve|s|d)', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']


def match(commit_text, regex):
    text = commit_text.lower()

    return len(re.findall(regex, text))


def regex_to_big_query(reg_exp
                       , text_field='message'):
    # TODO - check
    # Take care of encoding
    reg_exp = reg_exp.replace("\\", "\\\\").replace("'", "\\'")
    #reg_exp = reg_exp.replace("\\\\", "\\")
    # No need for grouping
    reg_exp = reg_exp.replace("(?:", "(")
    str = "(" + "LENGTH(REGEXP_REPLACE(lower(" + text_field + ")," + "'%s', '@'))" % reg_exp + "-" \
          + "LENGTH(REGEXP_REPLACE(lower(" + text_field + ")," + "'%s', ''))" % reg_exp + ")"

    return str


def generate_bq_function(func_name
                         , code_generator):
    print("# Run in Starndad sql ")
    print("CREATE OR REPLACE FUNCTION ")
    print(func_name)
    print(" (message string) ")
    print(" RETURNS int64 ")
    print("AS (")
    print("# Model language based on commit: XXX ")
    code_generator()
    print(" ) ")
    print(" ; ")



