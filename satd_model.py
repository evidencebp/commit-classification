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
#'hack',
'retarded'
, 'at a loss'
, 'stupid'
, 'remove this code'
, 'ugly'
, '(should|must|have to) take care'
, "(gone|is|went) wrong"
#, 'nuke'
, 'is problematic'
, 'may cause problem'
, 'hacky'
#, 'unknown why we ever experience this'
, 'soft error'
, 'silly'
, 'work(\s|-)?around'
, 'kludge'
#, 'fixme'
, "(isn't|not) quite right"
, 'trial and error'
#, 'give up'
, 'this is wrong'
#, 'hang our heads in shame'
, 'temporary (crutch|solution)'
, 'temporary'
, '(will cause|might cause) issue(s)?' # causes might be in present, part of a bug fix
, 'something bad'
, 'cause for issue'
, "this doesn't look right"
#, 'is this next line safe'
#, 'this indicates a more fundamental problem'
, 'this can be a mess'
, "(isn't|not) (very )?solid"
#, 'is this line really safe'
#, 'there is a problem'
#, 'some fatal error'
#, 'something serious is wrong'
, "don't use this"
, 'get rid of this'
, 'doubt that this would work'
, 'this is bs'
#, 'give up and go away'
, 'risk of this blowing up'
, 'just abandon it'
#, 'prolly a bug'
, 'probably a bug'
, 'hope everything will work'
, 'toss it'
#, 'barf'
#, 'something bad happened'
, 'fix this crap'
, 'yuck'
, 'certainly buggy'
, 'remove (me|it) before production'
#, 'you can be unhappy now'
, 'this is uncool'
#, 'bail out'
, "it doesn't work"
, 'crap'
, 'inconsistency'
, 'until fixed'
#, 'abandon all hope'
#, 'kaboom'
]

positive_terms = ['fixme'#, 'hack'
                 , 'low quality'
                 , 'tech(nical)?\sdebt'
                 , 'todo'
                 #, 'xxx'
                  ] + exploratory_terms

removal_terms = [
    'address' + REGULAR_SUFFIX
    , 'because'
    , 'clean' + REGULAR_SUFFIX
    , 'delet' + VERB_E_SUFFIX
    , '(do|does|did|doing)'
    , 'expand' + REGULAR_SUFFIX
    , 'finish' + REGULAR_SUFFIX
    , 'fix' + REGULAR_SUFFIX
    , 'implement' + REGULAR_SUFFIX
    , '(get|got|gets|getting)\srid'
    , 'list' + REGULAR_SUFFIX
    , 'mov' + VERB_E_SUFFIX
    , 'remov' + VERB_E_SUFFIX
    , 'replac' + VERB_E_SUFFIX
    , 'resolv' + VERB_E_SUFFIX
    , 'revert' + REGULAR_SUFFIX
    , 'updat' + VERB_E_SUFFIX
    , 'was'
]
excluded_terms = [
    'temporary(\s|_)(allocator|buffer|data|file|folder|list|location|place)(s)?'
    , 'temporary(\s|_)director(y|ies)'
    , 'todo.txt'
    , 'todo director(y|ies)'
    , 'todo folder(s)?'
    , 'todo list(s)?'
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
    print_concepts_functions_for_bq(commit='c5ba4cd1971da27f74ce1319415626143092d317')
    evaluate_satd_classifier()

    text = """
"Add new django tutorial (#4869)

* Cloud Run with Django tutorial

* Cloud Run with Django tutorial

* black, .env file update

* Document Dockerfile, add PYTHONUNBUFFERED

* Document cloudmigrate.yaml

* Formatiting

* Bump django, remove mysql

* Update secretmanager

* Update pinned dependencies

* ensure path is set correctly with api update

* format

* Generalise cloudmigrate file

* update service default

* add tests

* Update CODEOWNERS

* Licence headers

* Remove envvar declaration

* cleanup readme

* Fix import names, region tags

* black

* Cloud Run with Django tutorial

* black, .env file update

* Document Dockerfile, add PYTHONUNBUFFERED

* Document cloudmigrate.yaml

* Formatiting

* Bump django, remove mysql

* Update secretmanager

* Update pinned dependencies

* ensure path is set correctly with api update

* format

* Generalise cloudmigrate file

* update service default

* add tests

* Update CODEOWNERS

* Licence headers

* Remove envvar declaration

* cleanup readme

* Fix import names, region tags

* black

* black

* Format YAML

* bump dependencies

* Update var names, remove sql instance creation

* PR Feedback

* Debug failing command

* Remove IAM calls - possible permissions issues

* debug

* force local settings if in nox/test

* add IDs to cloud build

* Update region tags

* Get instance name from envvar

* Make secrets dynamic, optionally overload names by envvar

* Remove create/destroy of static setting

* Consolidate envvars

* fix region tags

* lint, import error

* Testing instance name is fqdn, need just name for gcloud sql calls

* Ensure project specified on gcloud calls

* set project when using gsutil

* order of flags in gsutil matters

* ensure all subprocesses include project

causes issues otherwise

* Add and remove more project tags

* Update comments

* match on exact project name, not substring

* lint

* Can't hide the settings name in the setting itself 🧐

* big oof

* migrations require __init__.py to be detected

* Bump overnight patch

* Debug 503

* Service requires custom settings envvar

* attempt fixing local tests

* lint

* revert accidental appengine change

* envvars

* ohno

* wrong varname

* Update run/django/noxfile_config.py

Co-authored-by: Leah E. Cole <a5082685b0b89abc4f85079ca3a58177707489f8@users.noreply.github.com>

* Add licence header

* Formatting

* black

* Add typehinting, remove debugging

* ⚠️  noxfile change - add typehints

* ⚠️ noxfile change - fix method signature

* ⚠️ noxfile change - fix nox session type

* ⚠️ noxfile change - import order

* hadolint Dockerfile

* revert hadolint

* Add linking

* Remove gcloudignore

* Testing: i have a theory this is why tests started failing

Co-authored-by: Leah E. Cole <a5082685b0b89abc4f85079ca3a58177707489f8@users.noreply.github.com>"
"
""".lower()
    print("Label", is_satd(text))
    print("concept in text", re.findall(build_positive_regex(), text))
    print("exclusion in text", re.findall(build_excluded_regex(), text))
    print(build_excluded_regex())
    #print("v1", re.findall("(update todo|(because|clean(?:s|ed|ing)?|delet(?:e|es|ed|ing)|fix(?:s|ed|ing)?|implement(?:s|ed|ing)?|(get|got|gets|getting)\srid|list(?:s|ed|ing)?|mov(?:e|es|ed|ing)|remov(?:e|es|ed|ing)|resolv(?:e|es|ed|ing)|updat(?:e|es|ed|ing)|was))[\S\s]{0,40}", text))
