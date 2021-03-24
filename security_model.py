"""
Sources:
https://arxiv.org/pdf/2001.09148.pdf

"""


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

# Not sure list
"""
"""

positive_terms = [
 'advisory',
 'anti(?: |-)virus(?:es)?',
 'attack(?:s)?',
 'auth',
 'authenticat(e|ion)',
 #'authorization', # consider
 #'brute force', # consider
 'bug bount(y|ies)',
 #'bypass(?:es|ed|ing)?', # mostly tests related
 'certificate(?:s)?',
 #'constant time', # too general
 'crack(?:s)?',
 'credential(s)?',
 'cross(?: |-)origin',
 'cross(?: |-)site',
 '(?:cryptographic|cryptography)',
 'cve(-d+)?(-d+)?',
 'clickjack',
 'cyber',
 'decrypt' + REGULAR_SUFFIX,
 'decryption',
 'denial of service',
 '(de)?serializ', # consider
 'directory traversal',
 'dos', # consider
 'encript' + REGULAR_SUFFIX,
 'encription',
 'ensur(?:e|es|ed|ing)(\sthe)?\ssafety',
 'exploit(?:s)?',
 'fire(?: |-)wall(?:s)?',
 #'expos(e|ing)',
 # 'hack', # A bit general, consider
 'hijack',
 #'harden(?:s|ed|ing)?',
 'https instead of http',
 #'infinite loop', # consider
 'injection', # consider
 '(in)?secur(e|ity)',
 'lockout',
 'malicious',
 'malware(?:s)?', #plural of malware is malware yet not all are aware
 'nvd' # NVD
 'open redirect',
 'osvdb', # OSVDB
 #'overflow', # usually general
 'password(?:s)?',
 'permission(?:s)?',
 #'poison(?:s|es|ed|ing)?', usually a library
 'port scan(?:s|ed|ing)?',
 'privilege(?:s)?',
 # 'proof of concept', # consider
 'rce', # remote code execution
 'redos' # ReDoS
 'remote code execution',
 'return oriented programming',
 #'root', # consider
 #'(?:safe|safety|unsafe|safer)',
 #'(?:safety|unsafe|safer)', # safe alone seems too general
'(?:safe|safety|unsafe|safer|github)\s(token|browser|protocol)(?:s)?',
 'secret(?:s)?',
 'security',
 'session fixation',
 'spoof(?:s|es|ed|ing)?',
 'threat(?:s|ed|ing)?',
 #'tls', # transport layer security, sometime too general
 #'timing', # consider
 #'token(?:s)?',
 #'traversal',
 'unauthori[z|s]ed',
 # 'username', # consider
 'vulnerable',
 'vulnerabilit(?:y|ies)',
 'x(?: |-)frame(?: |-)option(?:s)?',
 'xss',
 'xsrf', # XSRF
 'xxe' # XXE
    ]

excluded_terms = ['https://secure', # A too common link in commits
                  'error(?:s)? injection', # in tests
                  ]

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_security(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def security_to_bq():
    concept = 'security'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_{concept}(message)".format(schema=SCHEMA_NAME
                                                       , concept=concept))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_{concept}(message)".format(schema=SCHEMA_NAME
                                                           , concept=concept))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_{concept}(message)".format(schema=SCHEMA_NAME
                                                               , concept=concept))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concept = 'security'

    concepts = {'core_' + concept : build_positive_regex
        , 'excluded_' + concept : build_excluded_regex
        , 'not_positive_' + concept : build_not_positive_regex
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
                                                        , concept=concept)
                         , security_to_bq
                         , commit=commit)
    print()
def evaluate_security_classifier():

    evaluate_concept_classifier(concept='Security'
                                , text_name='message'
                                , classification_function=is_security
                                , samples_file=join(DATA_PATH, 'commit_security_samples.csv'))


if __name__ == '__main__':
    #print_concepts_functions_for_bq(commit='2be15899b72484a3927b01a57b476cf6e8b76188')
    evaluate_security_classifier()

    text = """
"Sensitivity plots fix (#2860)

* fix immediately obvious bug in plotting loop

* add in allinj plots, create front summary page

* move allinj to after injection plots loop

* Fix to make bank_plot work. Include found table in injection pages

* Use censored veto, clarify fixme comments

* add snrifar summary to main page

* remove confusing and unneccessary bit

* found table doesnt work

* fix up one thing which turned into a list although it's only a list with 1 entry

* add Gareth"
""".lower()
    print("is fix", is_security(text))
    print("security in text", re.findall(build_positive_regex(), text))


