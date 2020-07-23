

import re

from language_utils import file_scheme, term_seperator, build_sepereted_term, \
    regex_to_big_query, generate_bq_function, SCHEMA_NAME


def English_to_bq():

    print("# English")
    print( "# English :build_English_regex()")
    #print( ",")
    print( regex_to_big_query(build_English_regex()))

English_terms = ['about', 'all', 'also', 'and', 'because', 'but', 'can', 'come', 'could', 'day', 'even', 'find'
    , 'first', 'for', 'from', 'get', 'give', 'have', 'her', 'here', 'him', 'his', 'how', 'into', 'its', 'just', 'know'
    , 'like', 'look', 'make', 'man', 'many', 'more', 'new', 'not', 'now', 'one', 'only', 'other', 'our', 'out'
    , 'people', 'say', 'see', 'she', 'some', 'take', 'tell', 'than', 'that', 'the', 'their', 'them', 'then', 'there'
    , 'these', 'they', 'thing', 'think', 'this', 'those', 'time', 'two', 'use', 'very', 'want', 'way', 'well', 'what'
    , 'when', 'which', 'who', 'will', 'with', 'would', 'year', 'you', 'your']

def build_English_regex():
    Eng_re = "%s(%s)%s" % (term_seperator
                               , "|".join(English_terms)
                               , term_seperator)

    return Eng_re

def is_English(commit_text):
    text = commit_text.lower()

    English_num = len(re.findall(build_English_regex(), text))

    return English_num > 0


def Englis_to_bq():
    # TODO - the \n in the string seperator is printed as a new line and should be fixed
    print("# English")
    print( "# English : build_English_regex()")
    #print( ",")
    print( regex_to_big_query(build_English_regex()))
    print("#English - end")

def print_English_functions():
    print()
    generate_bq_function('{schema}.bq_English'.format(schema=SCHEMA_NAME), Englis_to_bq)
    print()

if __name__ == '__main__':
    print_English_functions()