"""
Sources:
https://arxiv.org/pdf/2001.09148.pdf

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
"""

positive_terms = [
 'advisory',
 'attack(?:s)?',
 'auth',
 'authenticat(e|ion)',
 'brute force', # consider
 'bug bount(y|ies)',
 'bypass(?:es|ed|ing)?', # consider
 'certificate(?:s)?',
 #'constant time', # too general
 'crack',
 'credential(s)?',
 'cross(?: |-)origin',
 'cross(?: |-)site',
 'cve(-d+)?(-d+)?',
 'clickjack',
 'cyber',
 'denial of service',
 '(de)?serializ', # consider
 'directory traversal',
 'dos', # consider
 'exploit',
 #'expos(e|ing)',
 # 'hack', # A bit general, consider
 'hijack',
 'harden',
 #'infinite loop', # consider
 'injection',
 '(in)?secur(e|ity)',
 'lockout',
 'malicious',
 'malware(?:s)?', #plural of malware is malware yet not all are aware
 'nvd' # NVD
 'open redirect',
 'osvdb', # OSVDB
 'overflow', # consider
 'password(?:s)?',
 'permission(?:s)?',
 'poison(?:s|es|ed|ing)?',
 'port scan',
 'privilege(?:s)?',
 # 'proof of concept', # consider
 'rce', # remote code execution
 'redos' # ReDoS
 'remote code execution',
 'return oriented programming',
 '(?:safe|safety|unsafe|safer)',
 'security',
 'session fixation',
 'spoof(?:s|es|ed|ing)?',
 'threat(?:s|ed|ing)?',
 'timing', # consider
 'token(?:s)?',
 #'traversal',
 'unauthori[z|s]ed',
 'vulnerabilit(?:y|ies)',
 'x(?: |-)frame(?: |-)option(?:s)?',
 'xss',
 'xsrf', # XSRF
 'xxe' # XXE
    ]


excluded_terms = ['_____PLACEHOLDER_____'
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

    evaluate_concept_classifier(concept='Swearing'
                                , text_name='message'
                                , classification_function=is_security
                                , samples_file=join(DATA_PATH, 'commit_security_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='079703f7a83e56a98d009570b52ca1f439f28081')
    #evaluate_security_classifier()

    text = """When triggering audits, count ""Accepted"" revisions as successfully reviewed

Summary:
See PHI1118. That issue may describe more than one bug, but the recent ordering changes to the import pipeline likely make this at least part of the problem.

Previously, commits would always close associated revisions before we made it to the ""publish"" step. This is no longer true, so we might be triggering audits on a commit before the associated revision actually closes.

Accommodate this by counting a revision in either ""Accepted"" or ""Published (Was Previously Accepted)"" as ""reviewed"".

Test Plan:
  - With commit C affecting paths in package P with ""Audit Unreviewed Commits and Commits With No Owner Involvement"", associated with revision R, with both R and C authored by the same user, and ""R"" in the state ""Accepted"", used `bin/repository reparse --publish <hash>` to republish the commit.
  - Before change: audit by package P triggered.
  - After change: audit by package P no longer triggered.

Reviewers: amckinley

Reviewed By: amckinley

Differential Revision: https://secure.phabricator.com/D20564

""".lower()
    print("is fix", is_security(text))
    print("security in text", re.findall(build_positive_regex(), text))


