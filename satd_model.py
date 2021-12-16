"""
A model for identifying Self Admitted Technical Debt (SATD)
"""

import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH, term_seperator
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier


# Based on the lists from
# Prevalence, Contents and Automatic Detection of KL-SATD by Leevi Rantala and Mika Mäntylä and David Lo
# An exploratory study on self-admitted technical debt by Potdar, Aniket and Shihab, Emad

exploratory_terms = [
'hack'
, 'retarded'
, 'at a loss'
, 'stupid'
, 'remove this code'
, 'ugly'
, 'take care'
, "something's gone wrong"
, 'nuke'
, 'is problematic'
, 'may cause problem'
, 'hacky'
, 'unknown why we ever experience this'
, 'treat this as a soft error'
, 'silly'
, 'workaround for bug'
, 'kludge'
, 'fixme'
, "this isn't quite right"
, 'trial and error'
, 'give up'
, 'this is wrong'
, 'hang our heads in shame'
, 'temporary solution'
, 'causes issue'
, 'something bad is going on'
, 'cause for issue'
, "this doesn't look right"
, 'is this next line safe'
, 'this indicates a more fundamental problem'
, 'temporary crutch'
, 'this can be a mess'
, "this isn't very solid"
, 'this is temporary and will go away'
, 'is this line really safe'
, 'there is a problem'
, 'some fatal error'
, 'something serious is wrong'
, "don't use this"
, 'get rid of this'
, 'doubt that this would work'
, 'this is bs'
, 'give up and go away'
, 'risk of this blowing up'
, 'just abandon it'
, 'prolly a bug'
, 'probably a bug'
, 'hope everything will work'
, 'toss it'
, 'barf'
, 'something bad happened'
, 'fix this crap'
, 'yuck'
, 'certainly buggy'
, 'remove me before production'
, 'you can be unhappy now'
, 'this is uncool'
, 'bail out'
, "it doesn't work yet"
, 'crap'
, 'inconsistency'
, 'abandon all hope'
, 'kaboom'
]

positive_terms = ['fixme', 'hack'
                 , 'todo'
                 , 'xxx'
                  ] #+ exploratory_terms

removal_terms = [
    'because'
    , 'clean' + REGULAR_SUFFIX
    , 'delet' + VERB_E_SUFFIX
    , 'expand' + REGULAR_SUFFIX
    , 'fix' + REGULAR_SUFFIX
    , 'implement' + REGULAR_SUFFIX
    , '(get|got|gets|getting)\srid'
    , 'list' + REGULAR_SUFFIX
    , 'mov' + VERB_E_SUFFIX
    , 'remov' + VERB_E_SUFFIX
    , 'resolv' + VERB_E_SUFFIX
    , 'updat' + VERB_E_SUFFIX
    , 'was'
]
excluded_terms = [
    'todo list(s)?'
    , 'todo note(s)?'
    , 'update todo'
    , "(%s)%s(%s)" % ("|".join(removal_terms), NEAR_ENOUGH, "|".join(positive_terms))
    , "(%s)(/|\.|=)" % ("|".join(positive_terms))
    , '\.xxx'
    , '=xxx'
                  ]

def build_positive_regex():

    #return "(%s)" % ("|".join(positive_terms))

    return build_sepereted_term(positive_terms)



def build_excluded_regex():
    #return "(%s)" % ("|".join(excluded_terms))
    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_satd(commit_text):
    #commit_text = re.sub(r"\s+", " ", commit_text.strip())
    text = commit_text.lower()

    return (len(re.findall(build_positive_regex(), text))
            - len(re.findall(build_excluded_regex(), text))
            - len(re.findall(build_not_positive_regex(), text)))  > 0



def satd_to_bq():
    concept = 'satd'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_satd(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_satd(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_satd(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):


    concepts = {'core_satd' : build_positive_regex
        , 'excluded_satd': build_excluded_regex
        , 'not_positive_satd' : build_not_positive_regex
        #, 'satd': satd_to_bq

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
                                                        , concept='satd')
                         , satd_to_bq
                         , commit=commit)
    print()
def evaluate_satd_classifier():

    evaluate_concept_classifier(concept='satd'
                                , text_name='message'
                                , classification_function=is_satd
                                , samples_file=join(DATA_PATH, 'satd_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='11b22c84b83172b515a8137ce42dda037858a637')
    evaluate_satd_classifier()

    text = """
"Logs will now be put in one file for both server and client (#880)

* Fixed error if NitroxLauncher things process has exited but actually it's still processing write.

* - Set Subnautica installation directory as default location for all Nitrox Logs (if available)
- Allowed for logs from either server or client to be in one log file
- Change log format to include logger name which equals to the executing application name

* Reduced server save logs

* Added todo to server save time to pause saving if no players are on
"
""".lower()
    print("Label", is_satd(text))
    print("concept in text", re.findall(build_positive_regex(), text))
    print("exclusion in text", re.findall(build_excluded_regex(), text))
    print(build_excluded_regex())
    #print("v1", re.findall("(update todo|(because|clean(?:s|ed|ing)?|delet(?:e|es|ed|ing)|fix(?:s|ed|ing)?|implement(?:s|ed|ing)?|(get|got|gets|getting)\srid|list(?:s|ed|ing)?|mov(?:e|es|ed|ing)|remov(?:e|es|ed|ing)|resolv(?:e|es|ed|ing)|updat(?:e|es|ed|ing)|was))[\S\s]{0,40}", text))
